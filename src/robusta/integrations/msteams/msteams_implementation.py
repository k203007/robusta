import json
import logging
import requests

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


    def __init__(self, msteams_hookurl: str, title: str, description: str):
        try:
            self.msteams_hookurl = msteams_hookurl
            self.myTeamsMessage = MsTeamsAdaptiveCard()
            self.myTeamsMessage.set_text_block(title, AdaptiveCardFontSize.EXTRA_LARGE)
            if description is not None:
                self.myTeamsMessage.set_text_block(description, AdaptiveCardFontSize.MEDIUM)
        except Exception as e:
            logging.error(f"Error creating MsTeamsAdaptiveCard: {e}")
            raise e

    def new_card_section(self):
        # write previous section
        self.__write_section_to_card()

    def __write_section_to_card(self):
        if self.current_section_string == '':
            return
        self.current_body_string += self.myTeamsMessage.get_section_separator()
        print(self.myTeamsMessage.get_section_separator())
        self.current_body_string += self.current_section_string
        self.current_section_string = ''

    def upload_files(self, file_blocks: list[FileBlock]):
        msteams_files = MsTeamsAdaptiveCardFiles()
        self.current_body_string += msteams_files.upload_files(file_blocks)

    def table(self, table_block : TableBlock):
        msteam_table = MsTeamsAdaptiveCardTable()
        table = msteam_table.create_table(self.__get_stretch_list_for_table(table_block.headers, False), table_block.headers, table_block.rows)
        self.current_section_string += table

    def list_of_strings(self, list_block: ListBlock):
        markdown_str_list = ''
        for text in list_block.items:
            markdown_str_list += '\n- ' + text + '\n'
        list_str = self.myTeamsMessage.get_text_block(markdown_str_list, AdaptiveCardFontSize.MEDIUM)
        self.current_section_string += list_str

    def diff(self, block: KubernetesDiffBlock):
        header_list = ['Previos Version', 'Current Version']
        rows = []
        for d in block.diffs:
            rows.append([d.other_value, d.value])
        msteam_table = MsTeamsAdaptiveCardTable()
        table = msteam_table.create_table(self.__get_stretch_list_for_table(header_list, True), header_list, rows)
        self.current_section_string += table

    def __get_stretch_list_for_table(self, header_list : list[str], stretch : bool):
        stretch_list = []
        for ix in range(len(header_list)):
            stretch_list.append(stretch)
        return stretch_list

    def markdown_block(self, block: BaseBlock):
        if not block.text:
            return
        text = self.__apply_length_limit(block.text) + self.__new_line_replacer('\n\n')
        self.current_section_string += self.myTeamsMessage.get_text_block(text, AdaptiveCardFontSize.MEDIUM)

    def divider_block(self, block: BaseBlock):
        self.current_section_string += self.__new_line_replacer('\n\n')

    def header_block(self, block: BaseBlock):
        current_header_string = self.__apply_length_limit(block.text, 150) + self.__new_line_replacer('\n\n')
        self.current_section_string += self.myTeamsMessage.get_text_block(current_header_string, AdaptiveCardFontSize.EXTRA_LARGE)

    def get_action_block_for_choices(self, choices: Dict[str, Callable] = None, context=""):
        if choices is None:
          return
        '''
        buttons = []
        for (i, (text, callback)) in enumerate(choices.items()):
            buttons.append(
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": text,
                    },
                    "style": "primary",
                    "action_id": f"{ACTION_TRIGGER_PLAYBOOK}_{i}",
                    "value": PlaybookCallbackRequest.create_for_func(
                        callback, context, text
                    ).json(),
                }
            )

        return [{"type": "actions", "elements": buttons}]
        '''

    def send(self):
        try:
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

