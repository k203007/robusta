import json
import logging
import tempfile

from .msteams_implementation import *
from ...core.model.events import *
from ...core.reporting.blocks import *
from ...core.reporting.utils import add_pngs_for_all_svgs
from ...core.reporting.callbacks import PlaybookCallbackRequest
from ...core.reporting.consts import SlackAnnotations
from ...core.model.env_vars import TARGET_ID

class MsTeamskSender:
    def __to_msteams(self, block: BaseBlock, msteams_single_msg: MsTeamsSingleMsg):
        if self.__same_type(block, MarkdownBlock):
            msteams_single_msg.markdown_block(block)
        elif self.__same_type(block, DividerBlock):
            msteams_single_msg.divider_block(block)
        elif self.__same_type(block, HeaderBlock):
            msteams_single_msg.header_block(block)
        elif self.__same_type(block, TableBlock):
            msteams_single_msg.table(block)
        elif self.__same_type(block, ListBlock):
            msteams_single_msg.list_of_strings(block)
        elif self.__same_type(block, KubernetesDiffBlock):
            msteams_single_msg.diff(block)
        elif self.__same_type(block, CallbackBlock):
            logging.error(
                f"CallbackBlock not supported for msteams"
            )
        else:
            logging.error(
                f"cannot convert block of type {type(block)} to msteams format block: {block}"
            )

    def __split_block_to_files_and_all_the_rest(self, enrichment : Enrichment):
        files_blocks = []
        other_blocks = []

        for block in enrichment.blocks:
            if self.__same_type(block,FileBlock):
                files_blocks.append(block)
            else:
                other_blocks.append(block)
        return files_blocks, other_blocks

    def __same_type(self, var, class_type):
        return type(var).__name__ == class_type.__name__

    def send_finding_to_msteams(self, msteams_hookurl: str, finding: Finding):
        msteams_single_msg = MsTeamsSingleMsg(msteams_hookurl, finding.title, finding.description)

        for enrichment in finding.enrichments:
                        
            files_blocks, other_blocks = self.__split_block_to_files_and_all_the_rest(enrichment)

            for block in other_blocks:
                self.__to_msteams(block, msteams_single_msg)

            msteams_single_msg.upload_files(files_blocks)

            msteams_single_msg.new_card_section()

        msteams_single_msg.send()