import json
import logging
import requests

from src.robusta.integrations.msteams.msteams_adaptive_card_elements import MsTeamsAdaptiveCardElements

from .msteams_adaptive_card_files import MsTeamsAdaptiveCardFiles
from .msteams_adaptive_card_table import MsTeamsAdaptiveCardTable
from .msteams_adaptive_card import AdaptiveCardFontSize,MsTeamsAdaptiveCard
from ...core.model.events import *
from ...core.reporting.blocks import *
from ...core.reporting.utils import add_pngs_for_all_svgs
from ...core.reporting.callbacks import PlaybookCallbackRequest
from ...core.reporting.consts import SlackAnnotations
from ...core.model.env_vars import TARGET_ID

ACTION_TRIGGER_PLAYBOOK = "trigger_playbook"
MsTeamsBlock = Dict[str, Any]

class MsTeamsImplementation:
    current_body_string = ''
    current_section_string = ''
    msteams_hookurl = ''

    card_content = [map]
    current_section = []

    elements = MsTeamsAdaptiveCardElements()

    def __init__(self, msteams_hookurl: str, title: str, description: str):
        self.msteams_hookurl = msteams_hookurl
        self.card_content.append(self.elements.text_block(text=title, font_size='extraLarge'))
        if description is not None:
            self.card_content.append(self.elements.text_block(text=description))

    def new_card_section(self):
        # write previous section
        self.__write_section_to_card()

    def __write_section_to_card(self):
        if len(self.current_section) == 0:
            return
        self.card_content.append(self.current_section)
        self.current_section = {}

    def __sub_section_separator(self):
        if len(self.current_section) == 0:
            return
        self.current_section_string += self.myTeamsMessage.get_sub_section_separator()

    def upload_files(self, file_blocks: list[FileBlock]):
        self.__sub_section_separator()
        msteams_files = MsTeamsAdaptiveCardFiles()
        self.current_section_string += msteams_files.upload_files(file_blocks)

    def table(self, table_block : TableBlock):
        self.__sub_section_separator()
        msteam_table = MsTeamsAdaptiveCardTable()
        table = msteam_table.create_table(table_block.headers, table_block.rows)
        self.current_section_string += table

    def list_of_strings(self, list_block: ListBlock):
        self.__sub_section_separator()
        for line in list_block.items:
            line_with_point = '\n- ' + line + '\n'
            self.current_section.append(self.elements.text_block(line_with_point))

    def diff(self, block: KubernetesDiffBlock):
        rows = []
        for d in block.diffs:
            row = f"*{d.formatted_path}*: {d.other_value} -> {d.value}"
            rows.append(row)
        list_blocks = ListBlock(rows)
        self.list_of_strings(list_blocks)

    def __get_stretch_list_for_table(self, header_list : list[str], stretch : bool):
        stretch_list = []
        for ix in range(len(header_list)):
            stretch_list.append(stretch)
        return stretch_list

    def markdown_block(self, block: BaseBlock):
        if not block.text:
            return
        text = self.__apply_length_limit(block.text) + self.__new_line_replacer('\n\n')
        self.current_section.append(self.elements.text_block(text))

    def divider_block(self, block: BaseBlock):
        self.current_section.append(self.elements.text_block(self.__new_line_replacer('\n\n')))

    def header_block(self, block: BaseBlock):
        current_header_string = self.__apply_length_limit(block.text, 150) + self.__new_line_replacer('\n\n')
        self.current_section.append(self.elements.text_block(current_header_string, font_size='large'))

    def get_action_block_for_choices(self, choices: Dict[str, Callable] = None, context=""):
        if choices is None:
          return

    def send(self):
        try:
            self.elements.card(xxxxxx)
            self.__write_section_to_card()

            response = requests.post(self.msteams_hookurl, data = self.myTeamsMessage.get_msg_to_send(self.current_body_string))
            print(response)
        except Exception as e:
            logging.error(f"error sending message to msteams\ne={e}\n")        


    def __apply_length_limit(self, msg: str, max_length: int = 3000):
        if len(msg) <= max_length:
            return msg
        truncator = "..."
        return self.__new_line_replacer(msg[: max_length - len(truncator)] + truncator)

    def __new_line_replacer(self, text : str):
        return text

