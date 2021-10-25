import uuid
from ...core.reporting.blocks import *

class MsTeamsAdaptiveCardFilesText:

    open_key_list = []
    close_start_key_list = []
    close_end_key_list = []
    text_file_presentaiton_key_list = []

    open_text_list = []
    close_start_text_list = []
    close_end_text_list = []
    text_file_presentaiton_text_list = []

    action_open_text_list = []
    action_close_start_text_list = []
    action_close_end_text_list = []


    def create_files_for_presentation(self, file_blocks: list[FileBlock]):
        file_name_list = []
        file_content_list = []

        for file_block in file_blocks:
            if not self.__its_txt_file(file_block.filename):
                continue
            self.__create_new_keys()
            file_name_list.append(file_block.filename)
            file_content_list.append(file_block.contents)

        if len(self.open_key_list) == 0:
            return ''

        for index in range(len(self.open_key_list)):
            self.__manage_blocks_for_single_file(index, file_name_list[index], file_content_list[index])
        print(self.__manage_all_text_to_send())
        return self.__manage_all_text_to_send()

    def __create_new_keys(self):
        self.open_key_list.append(str(uuid.uuid4()))
        self.close_start_key_list.append(str(uuid.uuid4()))
        self.close_end_key_list.append(str(uuid.uuid4()))
        self.text_file_presentaiton_key_list.append(str(uuid.uuid4()))

    def __manage_blocks_for_single_file(self, index, file_name : str, content : bytes):
        visible_when_open_pressed_list = [self.close_start_key_list[index], self.close_end_key_list[index], self.text_file_presentaiton_key_list[index]]
        visible_when_close_pressed_list = [self.open_key_list[index]]

        open_text_action = self.__action(visible_when_open_pressed_list)
        close_text_action = self.__action(visible_when_close_pressed_list)

        open_text = self.__create_txt_block_for_open_close(self.open_key_list[index], True, 'open ' + file_name)
        close_start = self.__create_txt_block_for_open_close(self.close_start_key_list[index], True, 'close ' + file_name)
        close_end = self.__create_txt_block_for_open_close(self.close_end_key_list[index], True, 'close ' + file_name)

        self.open_text_list.append(open_text)
        self.close_start_text_list.append(close_start)
        self.close_end_text_list.append(close_end)

        self.action_open_text_list.append(open_text_action)
        self.action_close_start_text_list.append(close_text_action)
        self.action_close_end_text_list.append(close_text_action)


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
          "spacing": "large",
          "items": [{0}],
          {1}
        }},
        '''

        top_files_line = ''
        items_text = ''
        for index in range(len(self.open_text_list)):
            items_text += single_column.format(self.open_text_list[index], self.action_open_text_list[index])
            items_text += single_column.format(self.close_start_text_list[index], self.action_close_start_text_list[index])
        top_files_line = block.format(items_text)

        bottom_files_line = ''
        items_text = ''
        for index in range(len(self.close_end_text_list)):
            items_text += single_column.format(self.close_end_text_list[index], self.action_close_end_text_list[index])
        bottom_files_line = block.format(items_text)

        return top_files_line +  bottom_files_line

    def __action(self, visible_keys: list[str]):
        toggle_block = '''
            "selectAction": {{
                    "type": "Action.ToggleVisibility",
                    "title": "dont care",
                    "targetElements": [{0}]
            }},
        '''

        single_element_block = '''
        {{ "elementId": "{0}", "visible": {1}
        }},
        '''

        all_keys_list = []
        all_keys_list.append(self.open_key_list)
        all_keys_list.append(self.close_start_key_list)
        all_keys_list.append(self.close_end_key_list)
        all_keys_list.append(self.text_file_presentaiton_key_list)

        elements = ''
        for key in visible_keys:
            vis_text = 'false'
            if key in all_keys_list:
                vis_text = 'true'
            elements += single_element_block.format(key, vis_text)

        return toggle_block.format(elements)

    def __create_txt_block_for_open_close(self, key : str, visible : bool, text : str):
        visible_text = 'false'
        if visible:
            visible_text = 'true'

        block = '''
        {{
            "type": "TextBlock",
            "text": "{0}",
            "isSubtle": false,
            "visible" : {1},
            "id" : "{2}",
        }},
        '''

        return block.format(text, visible_text, key)

    def __present_text_file_block(self, text : str):
        block = '''
        {{
            "type": "TextBlock",
            "text": "<blockquote>{0}</blockquote>",
            "visible" : false,
            "id" : {2}
        }},
        '''
        pass

    def __its_txt_file(self, file_name: str):
        txt_prefix_list = ['.txt', '.json']
        if file_name[-4:] in txt_prefix_list:
            return True
        return False
