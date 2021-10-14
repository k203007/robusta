import json
import logging
import tempfile
import pymsteams

from .msteams_implementation import *
from ...core.model.events import *
from ...core.reporting.blocks import *
from ...core.reporting.utils import add_pngs_for_all_svgs
from ...core.reporting.callbacks import PlaybookCallbackRequest
from ...core.reporting.consts import SlackAnnotations
from ...core.model.env_vars import TARGET_ID

MsTeamsBlock = Dict[str, Any]

class MsTeamskSender:
    msteams_hookurl = ''
    def __init__(self, msteams_hookurl: str):
        self.msteams_hookurl = msteams_hookurl

    def __to_msteams(self, block: BaseBlock):
        if isinstance(block, MarkdownBlock):
            self.msteams_implementation.markdown_block(self.myTeamsMessage, block)
        elif isinstance(block, DividerBlock):
            self.msteams_implementation.divider_block(self.myTeamsMessage, block)
        elif isinstance(block, FileBlock):
            raise AssertionError("to_msteams() should never be called on a FileBlock")
        elif isinstance(block, HeaderBlock):
            self.msteams_implementation.header_block(self.myTeamsMessage, block)
        elif isinstance(block, ListBlock) or isinstance(block, TableBlock):
            self.__to_msteams(block.to_markdown())
        elif isinstance(block, KubernetesDiffBlock):
            self.msteams_implementation.diff(self.myTeamsMessage, block)
        elif isinstance(block, CallbackBlock):
            context = block.context.copy()
            context["target_id"] = TARGET_ID
            self.msteams_implementation.get_action_block_for_choices(self.myTeamsMessage,
                block.choices, json.dumps(context)
            )
        else:
            logging.error(
                f"cannot convert block of type {type(block)} to msteams format block: {block}"
            )

    def __upload_file_to_msteams(self, block: FileBlock) -> str:
        """Upload a file to msteams and return a link to it"""
        # TODO: how to upload
        with tempfile.NamedTemporaryFile() as f:
            f.write(block.contents)
            f.flush()
            result = self.slack_client.files_upload(
                title=block.filename, file=f.name, filename=block.filename
            )
            return result["file"]["permalink"]

    def __upload_files(self, report_blocks: List[BaseBlock] = []):
        file_blocks = add_pngs_for_all_svgs(
            [b for b in report_blocks if isinstance(b, FileBlock)]
        )
        if not file_blocks:
            return
        uploaded_files = []
        for file_block in file_blocks:
            permalink = self.__upload_file_to_msteams(file_block)
            uploaded_files.append(f"* <{permalink} | {file_block.filename}>")

        file_references = "\n".join(uploaded_files)

    def __send_blocks_to_msteams(
        self,
        report_blocks: List[BaseBlock],
        report_attachment_blocks: List[BaseBlock],
    ):
        other_blocks = [b for b in report_blocks if not isinstance(b, FileBlock)]
        for block in other_blocks:
            self.__to_msteams(block)
        for block in report_attachment_blocks:
            self.__to_msteams(block)

    def __create_new_card(self, title: str, description: str):
        self.msteams_implementation = MsTeamsImplementation(self.msteams_hookurl, title, description)        

    def __prepare_msteams_card(self, finding: Finding):
        blocks: List[BaseBlock] = []
        # first add finding description block
        if finding.description:
            blocks.append(MarkdownBlock(finding.description))

        self.__create_new_card(finding.title, finding.description)


    def send_finding_to_msteams(self, finding: Finding):

        self.__prepare_msteams_card(finding)

        for enrichment in finding.enrichments:
            
            blocks: List[BaseBlock] = []
            attachment_blocks: List[BaseBlock] = []

            # TODO: what is this ??? SlackAnnotations.ATTACHMENT
            if enrichment.annotations.get(SlackAnnotations.ATTACHMENT):
                attachment_blocks.extend(enrichment.blocks)
            else:
                blocks.extend(enrichment.blocks)
            
            self.__send_blocks_to_msteams(blocks, attachment_blocks)

            self.__upload_files(blocks)

            self.msteams_implementation.new_card_section()

        self.msteams_implementation.send()

        
