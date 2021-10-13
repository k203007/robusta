import json
import logging
import tempfile
import pymsteams

from hikaru import DiffType

from .msteams_implementation import *
from ...core.model.events import *
from ...core.reporting.blocks import *
from ...core.reporting.utils import add_pngs_for_all_svgs
from ...core.reporting.callbacks import PlaybookCallbackRequest
from ...core.reporting.consts import SlackAnnotations
from ...core.model.env_vars import TARGET_ID

MsTeamsBlock = Dict[str, Any]

class MsTeamskSender:
    def __init__(self, msteams_hookurl: str):
        try:
            self.myTeamsMessage = pymsteams.connectorcard(msteams_hookurl)
        except Exception as e:
            logging.error(f"Cannot connect to MsTeams Channel: {e}")
            raise e

    def __to_slack(self, block: BaseBlock, sink_name: str) -> List[MsTeamsBlock]:        
        if isinstance(block, MarkdownBlock):
            MsTeamsImplementation.__markdown_block(self.myTeamsMessage, block)
        elif isinstance(block, DividerBlock):
            MsTeamsImplementation.__divider_block(self.myTeamsMessage, block)
        elif isinstance(block, FileBlock):
            raise AssertionError("to_slack() should never be called on a FileBlock")
        elif isinstance(block, HeaderBlock):
            MsTeamsImplementation.__header_block(self.myTeamsMessage, block)
        elif isinstance(block, ListBlock) or isinstance(block, TableBlock):
            return self.__to_slack(block.to_markdown(), sink_name)
        elif isinstance(block, KubernetesDiffBlock):
            return self.__to_slack_diff(self.myTeamsMessage, block)
        elif isinstance(block, CallbackBlock):
            context = block.context.copy()
            context["target_id"] = TARGET_ID
            context["sink_name"] = sink_name
            return MsTeamsImplementation.__get_action_block_for_choices(self.myTeamsMessage,
                block.choices, json.dumps(context)
            )
        else:
            logging.error(
                f"cannot convert block of type {type(block)} to slack format block: {block}"
            )
            return []  # no reason to crash the entire report

    def __to_slack_diff(self, card: pymsteams.connectorcard, block: KubernetesDiffBlock, sink_name: str) -> List[MsTeamsBlock]:
      # this can happen when a block.old=None or block.new=None - e.g. the resource was added or deleted
      if not block.diffs:
          return []

      slack_blocks = []
      slack_blocks.extend(
          MsTeamsImplementation.__to_slack(
              ListBlock(
                  [
                      f"*{d.formatted_path}*: {d.other_value} :arrow_right: {d.value}"
                      for d in block.diffs
                  ]
              ),
              sink_name,
          )
      )

      return slack_blocks


    def __upload_file_to_slack(self, block: FileBlock) -> str:
        """Upload a file to slack and return a link to it"""
        with tempfile.NamedTemporaryFile() as f:
            f.write(block.contents)
            f.flush()
            result = self.slack_client.files_upload(
                title=block.filename, file=f.name, filename=block.filename
            )
            return result["file"]["permalink"]

    def prepare_slack_text(self, message: str, files: List[FileBlock] = []):
        if files:
            # it's a little annoying but it seems like files need to be referenced in `title` and not just `blocks`
            # in order to be actually shared. well, I'm actually not sure about that, but when I tried adding the files
            # to a separate block and not including them in `title` or the first block then the link was present but
            # the file wasn't actually shared and the link was broken
            uploaded_files = []
            for file_block in files:
                permalink = self.__upload_file_to_slack(file_block)
                uploaded_files.append(f"* <{permalink} | {file_block.filename}>")

            file_references = "\n".join(uploaded_files)
            message = f"{message}\n{file_references}"

        if len(message) == 0:
            return "empty-message"  # blank messages aren't allowed

        return MsTeamskSender.__apply_length_limit(message)

    def __send_blocks_to_slack(
        self,
        report_blocks: List[BaseBlock],
        report_attachment_blocks: List[BaseBlock],
        title: str,
        slack_channel: str,
        unfurl: bool,
        sink_name: str,
    ):
        file_blocks = add_pngs_for_all_svgs(
            [b for b in report_blocks if isinstance(b, FileBlock)]
        )
        other_blocks = [b for b in report_blocks if not isinstance(b, FileBlock)]

        message = self.prepare_slack_text(title, file_blocks)

        output_blocks = []
        if title:
            output_blocks.extend(self.__to_slack(HeaderBlock(title), sink_name))
        for block in other_blocks:
            output_blocks.extend(self.__to_slack(block, sink_name))
        attachment_blocks = []
        for block in report_attachment_blocks:
            attachment_blocks.extend(self.__to_slack(block, sink_name))

        logging.debug(
            f"--sending to msteams--\n"
            f"title:{title}\n"
            f"blocks: {output_blocks}\n"
            f"attachment_blocks: {report_attachment_blocks}\n"
            f"message:{message}"
        )

        try:
            self.myTeamsMessage.send()

        except Exception as e:
            logging.error(
                f"error sending message to msteams\ne={e}\ntext={message}\nblocks={output_blocks}\nattachment_blocks={attachment_blocks}"
            )

    def send_finding_to_slack(
        self, finding: Finding, slack_channel: str, sink_name: str
    ):
        blocks: List[BaseBlock] = []
        attachment_blocks: List[BaseBlock] = []
        # first add finding description block
        if finding.description:
            blocks.append(MarkdownBlock(finding.description))

        unfurl = True
        for enrichment in finding.enrichments:
            # if one of the enrichment specified unfurl=False, this slack message will contain unfurl=False
            unfurl = unfurl and enrichment.annotations.get(
                SlackAnnotations.UNFURL, True
            )
            if enrichment.annotations.get(SlackAnnotations.ATTACHMENT):
                attachment_blocks.extend(enrichment.blocks)
            else:
                blocks.extend(enrichment.blocks)

        self.__send_blocks_to_slack(
            blocks, attachment_blocks, finding.title, slack_channel, unfurl, sink_name
        )
