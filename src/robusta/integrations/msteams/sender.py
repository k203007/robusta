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
    def __to_msteams(self, block: BaseBlock):
        if self.__same_type(block, MarkdownBlock):
            self.msteams_implementation.markdown_block(block)
        elif self.__same_type(block, DividerBlock):
            self.msteams_implementation.divider_block(block)
        elif self.__same_type(block, HeaderBlock):
            self.msteams_implementation.header_block(block)
        elif self.__same_type(block, TableBlock):
            self.msteams_implementation.table(block)
        elif self.__same_type(block, ListBlock):
            self.msteams_implementation.list_of_strings(block)
        elif self.__same_type(block, KubernetesDiffBlock):
            self.msteams_implementation.diff(block)
        elif self.__same_type(block, CallbackBlock):
            context = block.context.copy()
            context["target_id"] = TARGET_ID
            self.msteams_implementation.get_action_block_for_choices(self.myTeamsMessage,
                block.choices, json.dumps(context)
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

    def send_finding_to_msteams(self, msteams_implementation: MsTeamsImplementation, finding: Finding):
        self.msteams_implementation = msteams_implementation
        for enrichment in finding.enrichments:
            
            self.msteams_implementation.new_card_section()
            
            files_blocks, other_blocks = self.__split_block_to_files_and_all_the_rest(enrichment)

            for block in other_blocks:
                self.__to_msteams(block)

            self.msteams_implementation.upload_files(files_blocks)

        self.msteams_implementation.send()

        
