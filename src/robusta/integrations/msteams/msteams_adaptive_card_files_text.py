import uuid

from .msteams_adaptive_card_elements import MsTeamsAdaptiveCardElements, msteams_adaptive_card_elements
from ...core.reporting.blocks import *

class MsTeamsAdaptiveCardFilesText:

    open_key_list = []
    close_start_key_list = []
    close_end_key_list = []
    text_file_presentaiton_key_list = []

    open_text_list = []
    close_start_text_list = []
    close_end_text_list = []
    text_file_presentaiton_text = ''

    action_open_text_list = []
    action_close_start_text_list = []
    action_close_end_text_list = []

    file_name_list = []        

    elements = MsTeamsAdaptiveCardElements()

    def create_files_for_presentation(self, file_blocks: list[FileBlock]):
        file_content_list = []

        for file_block in file_blocks:
            if not self.__its_txt_file(file_block.filename):
                continue
            self.__create_new_keys()
            self.file_name_list.append(file_block.filename)
            file_content_list.append(file_block.contents)

        if len(self.open_key_list) == 0:
            return ''

        for index in range(len(self.open_key_list)):
            self.__manage_blocks_for_single_file(index, self.file_name_list[index], file_content_list[index])
        return self.__manage_all_text_to_send()

    def __create_new_keys(self):
        self.open_key_list.append(str(uuid.uuid4()))
        self.close_start_key_list.append(str(uuid.uuid4()))
        self.close_end_key_list.append(str(uuid.uuid4()))
        self.text_file_presentaiton_key_list.append(str(uuid.uuid4()))

    def __manage_blocks_for_single_file(self, index, file_name : str, content : bytes):
        open_text_action = self.__action(index, True, 'press to open')
        close_text_action = self.__action(index, False, 'press to close')

        open_text = self.elements.text_block('***open ' + file_name + '***', isSubtle=False)
        close_start = self.elements.text_block('***close ' + file_name + '***', isSubtle=False)
        close_end = self.elements.text_block('***close ' + file_name + '***', isSubtle=False)

        self.open_text_list.append(open_text)
        self.close_start_text_list.append(close_start)
        self.close_end_text_list.append(close_end)

        self.action_open_text_list.append(open_text_action)
        self.action_close_start_text_list.append(close_text_action)
        self.action_close_end_text_list.append(close_text_action)

        self.text_file_presentaiton_text += self.__present_text_file_block(self.text_file_presentaiton_key_list[index], content.decode('utf-8'))

    def __manage_all_text_to_send(self):
        block = '''
        {{
        "type": "ColumnSet",
        "columns": [{0}]
        }},
        '''

        single_column = '''
        {{
          "type": "Column",
          "width": "{3}px",
          "items": [{0}],
          "isVisible": {1},
          "id": "{2}",
          {4}
        }},
        '''

        top_files_line = ''
        items_text = ''
        for index in range(len(self.open_text_list)):
            width = self.__calc_file_name_width(index)
            xxxxxxxxxx
            items_text += single_column.format(self.open_text_list[index], 'true', self.open_key_list[index],  width,  self.action_open_text_list[index])
            items_text += single_column.format(self.close_start_text_list[index],  'false', self.close_start_key_list[index], width, self.action_close_start_text_list[index])            
        top_files_line = block.format(items_text)

        bottom_files_line = ''
        items_text = ''
        for index in range(len(self.close_end_text_list)):
            width = self.__calc_file_name_width(index)
            items_text += single_column.format(self.close_end_text_list[index], 'false', self.close_end_key_list[index], width, self.action_close_end_text_list[index])
        bottom_files_line = block.format(items_text)

        return top_files_line + self.text_file_presentaiton_text +  bottom_files_line
    
    # need to calc the approximate size of the file name + the prefix, otherwise it will spread on the entire line
    def __calc_file_name_width(self, index):
        # taking the max letters so there wont be movement in textblock
        prefix_letters = 'close '
        width = 7 * len(prefix_letters + self.file_name_list[index]) + 40
        return str(width)

    def __action(self, index, open : bool, title : str):
        elements = []
        curr_key = self.open_key_list[index]
        for key in self.open_key_list:
            visible = (not open) or (curr_key != key)
            elements.append(self.elements.action_toggle_target_elements([key], [visible]))

        curr_key = self.close_start_key_list[index]
        for key in self.close_start_key_list:
            visible = False
            visible = open and (curr_key == key)
            elements.append(self.elements.action_toggle_target_elements([key], [visible]))

        curr_key = self.close_end_key_list[index]
        for key in self.close_end_key_list:
            visible = False
            visible = open and (curr_key == key)
            elements.append(self.elements.action_toggle_target_elements([key], [visible]))

        curr_key = self.text_file_presentaiton_key_list[index]
        for key in self.text_file_presentaiton_key_list:
            visible = open and (curr_key == key)
            elements.append(self.elements.action_toggle_target_elements([key], [visible]))

        return self.elements.action (title=title, target_elements=elements)

    def __present_text_file_block(self, key : str, text : str):
        text_blocks = []
        for line in text.split('\n'):
            text_blocks.append(self.elements.text_block(text, wrap=True, weight='bolder'))
        return self.elements(key=key, items=text_blocks)


    def __its_txt_file(self, file_name: str):
        txt_prefix_list = ['.txt', '.json', 'yaml']
        if file_name[-4:] in txt_prefix_list:
            return True
        return False