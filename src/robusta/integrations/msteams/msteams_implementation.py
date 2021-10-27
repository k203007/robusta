import json
import logging
import requests
from collections.abc import Mapping

from src.robusta.integrations.msteams.msteams_adaptive_card_elements import MsTeamsAdaptiveCardElements

from .msteams_adaptive_card_files import MsTeamsAdaptiveCardFiles
from .msteams_adaptive_card_table import MsTeamsAdaptiveCardTable
from ...core.model.events import *
from ...core.reporting.blocks import *
from ...core.reporting.utils import add_pngs_for_all_svgs
from ...core.model.env_vars import TARGET_ID

ACTION_TRIGGER_PLAYBOOK = "trigger_playbook"
MsTeamsBlock = Dict[str, Any]

class MsTeamsImplementation:
    msteams_hookurl = ''

    card_content = []
    current_section = []

    elements = MsTeamsAdaptiveCardElements()

    def __init__(self, msteams_hookurl: str, title: str, description: str):
        self.msteams_hookurl = msteams_hookurl
        block = self.elements.text_block(text=title, font_size='extraLarge')
        self.__write_blocks_to_dict(self.card_content, block)
        if description is not None:
            block = self.elements.text_block(text=description)
            self.__write_blocks_to_dict(self.card_content, block)

    def new_card_section(self):
        # write previous section
        self.__write_section_to_card()

    def __write_section_to_card(self):
        if len(self.current_section) == 0:
            return

        space_block = self.elements.text_block(text=' ', font_size='small')
        separator_block = self.elements.text_block(text=' ',separator=True)
        column_block = self.elements.column(items=[space_block,separator_block], width_strech= True)
        column_set_block = self.elements.column_set([column_block])

        self.__write_blocks_to_dict(self.card_content, column_set_block)
        self.__write_blocks_to_dict(self.card_content, self.current_section)
        self.current_section = {}

    def __write_blocks_to_dict(self, dict : list[map], blocks):
        print(type(blocks))
        if isinstance(blocks, Mapping):
            if blocks:
                dict.append(blocks)
            return
        for block in blocks:
            if block:
                dict.append(block)

    def __sub_section_separator(self):
        if len(self.current_section) == 0:
            return
        space_block = self.elements.text_block(text=' ', font_size='small')
        separator_block = self.elements.text_block(text='_' * 30, font_size='small', horizontalAlignment='center')

        self.__write_blocks_to_dict(self.current_section, [space_block,separator_block,space_block,space_block])

    def upload_files(self, file_blocks: list[FileBlock]):
        self.__sub_section_separator()
        msteams_files = MsTeamsAdaptiveCardFiles()
        block_list : list = msteams_files.upload_files(file_blocks)
        self.__write_blocks_to_dict(self.current_section, block_list)

    def table(self, table_block : TableBlock):
        self.__sub_section_separator()
        msteam_table = MsTeamsAdaptiveCardTable()
        table = msteam_table.create_table(table_block.headers, table_block.rows)
        self.__write_blocks_to_dict(self.current_section, table)

    def list_of_strings(self, list_block: ListBlock):
        self.__sub_section_separator()
        for line in list_block.items:
            line_with_point = '\n- ' + line + '\n'
            self.__write_blocks_to_dict(self.current_section, self.elements.text_block(line_with_point))

    def diff(self, block: KubernetesDiffBlock):
        rows = []
        for d in block.diffs:
            row = f"*{d.formatted_path}*: {d.other_value} -> {d.value}"
            rows.append(row)
        list_blocks = ListBlock(rows)
        self.list_of_strings(list_blocks)

    def markdown_block(self, block: BaseBlock):
        if not block.text:
            return
        text = self.__apply_length_limit(block.text) + self.__new_line_replacer('\n\n')
        self.__write_blocks_to_dict(self.current_section, self.elements.text_block(text))

    def divider_block(self, block: BaseBlock):
        self.__write_blocks_to_dict(self.current_section, self.elements.text_block(self.__new_line_replacer('\n\n')))

    def header_block(self, block: BaseBlock):
        current_header_string = self.__apply_length_limit(block.text, 150) + self.__new_line_replacer('\n\n')
        self.__write_blocks_to_dict(self.current_section, self.elements.text_block(current_header_string, font_size='large'))

    def get_action_block_for_choices(self, choices: Dict[str, Callable] = None, context=""):
        if choices is None:
          return

    def send(self):
        try:
            self.__write_section_to_card()
            json_map = self.elements.card(self.card_content)
            print(json.dumps(json_map, indent=4))
            response = requests.post(self.msteams_hookurl, json= json_map)
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

