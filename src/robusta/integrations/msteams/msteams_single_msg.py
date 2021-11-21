import json
import logging
import requests
from collections.abc import Mapping

from .msteams_adaptive_card_elements import MsTeamsAdaptiveCardElements
from .msteams_elements.msteams_base_element import MsTeamsBaseElement
from .msteams_adaptive_card_files import MsTeamsAdaptiveCardFiles
from .msteams_elements.msteams_table_element import MsTeamsTableElement
from ...core.model.events import *
from ...core.reporting.blocks import *

ACTION_TRIGGER_PLAYBOOK = "trigger_playbook"

class MsTeamsSingleMsg:
    # actual size according to the DOC is ~28K.
    # it's hard to determine the real size because for example there can be large images that doesn't count
    # and converting the map to json doesn't give us an exact indication of the size so we need to take 
    # a safe zone of less then 28K
    MAX_SIZE_IN_BYTES = (1024 * 20)
    msteams_hookurl = ''

    def __init__(self, msteams_hookurl: str):
        self.entire_msg : list[MsTeamsBaseElement] = []
        self.current_section : list[MsTeamsBaseElement] = []

        self.text_map_and_single_text_lines_list__for_text_files = []
        self.url_image_map__for_image_files = []

        self.elements = MsTeamsAdaptiveCardElements()
        self.msteams_hookurl = msteams_hookurl

    def write_title_and_desc(self, title: str, description: str):
        block = self.elements.text_block(text=title, font_size='extraLarge')
        self.__write_to_entire_msg(block)
        
        if description is not None:
            block = self.elements.text_block(text=description)
            self.__write_to_entire_msg(block)

    def write_current_section(self):
        if len(self.current_section) == 0:
            return

        # TODO: elements
        space_block = self.elements.text_block(text=' ', font_size='small')
        separator_block = self.elements.text_block(text=' ',separator=True)
        column_block = self.elements.column(items=[space_block,separator_block], width_strech= True)
        underline_block = self.elements.column_set([column_block])

        self.__write_to_entire_msg(underline_block)
        self.__write_to_entire_msg(self.current_section)
        self.current_section = []

    def __write_to_entire_msg(self, blocks : list[MsTeamsBaseElement]):
        self.entire_msg += blocks

    def __write_to_current_section(self, blocks : list[MsTeamsBaseElement]):
        self.current_section += blocks

    # TODO: elements
    def __sub_section_separator(self):
        if len(self.current_section) == 0:
            return
        space_block = self.elements.text_block(text=' ', font_size='small')
        separator_block = self.elements.text_block(text='_' * 30, font_size='small', horizontalAlignment='center')
        self.__write_to_current_section([space_block,separator_block,space_block,space_block])

    # TODO - return list of elements - remove all lines
    def upload_files(self, file_blocks: list[FileBlock]):
        msteams_files = MsTeamsAdaptiveCardFiles()
        block_list : list = msteams_files.upload_files(file_blocks)
        if len(block_list) > 0:
            self.__sub_section_separator()

        self.text_map_and_single_text_lines_list__for_text_files += \
            msteams_files.get_text_map_and_single_text_lines_list__for_text_files()
        self.url_image_map__for_image_files += msteams_files.get_url_map_list()
        
        self.__write_to_current_section(block_list)

    def table(self, table_block : TableBlock):
        self.__sub_section_separator()
        msteam_table = MsTeamsTableElement(table_block.headers, table_block.rows)
        self.__write_to_current_section(msteam_table)
    
    # TODO: apply length limit
    # TODO: CHECK IF THERE IS LIMIT IN TEXT BLOCK - IF NOT DELETE APPLY_LENGTH_LIMIT
    def list_of_strings(self, list_block: ListBlock):
        self.__sub_section_separator()
        for line in list_block.items:
            line_with_point = '\n- ' + line + '\n'
            self.__write_to_current_section(self.elements.text_block(line_with_point))

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
        self.__write_to_current_section(self.elements.text_block(text))

    def divider_block(self, block: BaseBlock):
        self.__write_to_current_section(self.elements.text_block(self.__new_line_replacer('\n\n')))

    def header_block(self, block: BaseBlock):
        current_header_string = self.__apply_length_limit(block.text, 150) + self.__new_line_replacer('\n\n')
        self.__write_to_current_section(self.elements.text_block(current_header_string, font_size='large'))

    # dont include the base 64 images in the total size calculation
    # TODO: ELEMENT of textfileElement
    def _put_text_files_data_up_to_max_limit(self, card_map : map):
        curr_images_len = 0
        for image_map in self.url_image_map__for_image_files:
            curr_images_len += self.elements.get_image_url_size(image_map)
        max_len_left = self.MAX_SIZE_IN_BYTES - (self.__get_current_card_len(card_map) - curr_images_len)

        curr_line = 0
        while True:
            line_added = False
            curr_line += 1            
            for text_map, lines in self.text_map_and_single_text_lines_list__for_text_files:
                if len(lines) < curr_line:
                    continue
                line = lines[len(lines) - curr_line]
                max_len_left -= len(line)
                if max_len_left < 0:
                    return
                new_text_value = line + self.elements.get_text_from_block(text_map)
                self.elements.set_text_from_block(text_map, new_text_value)
                line_added = True
            if not line_added:
                return

    def send(self):
        try:
            self.write_current_section()

            complete_card_map = self.elements.card(self.entire_msg)
            self._put_text_files_data_up_to_max_limit(complete_card_map)

            #print(json.dumps(complete_card_map, ensure_ascii=False))      
            # print(self.__get_current_card_len(complete_card_map))
            response = requests.post(self.msteams_hookurl, json= complete_card_map)
            if 'error' in response.content.decode():
                print('failed !!!')
                raise Exception('error in sending: ' + response.content.decode()) 
            print('success...')            

        except Exception as e:
            logging.error(f"error sending message to msteams\ne={e}\n")   

    def __get_current_card_len(self, complete_card_map : map):
        return len(json.dumps(complete_card_map, ensure_ascii=True, indent=2))

    def __apply_length_limit(self, msg: str, max_length: int = 3000):
        if len(msg) <= max_length:
            return msg
        truncator = "..."
        return self.__new_line_replacer(msg[: max_length - len(truncator)] + truncator)

    def __new_line_replacer(self, text : str):
        return text

