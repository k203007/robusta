import uuid

from .msteams_adaptive_card_elements import MsTeamsAdaptiveCardElements
from ...core.reporting.blocks import *

class MsTeamsAdaptiveCardFilesText:

    open_key_list = []
    close_start_key_list = []
    close_end_key_list = []
    text_file_presentaiton_key_list = []

    open_text_list = []
    close_start_text_list = []
    close_end_text_list = []
    text_file_presentaiton_list = []

    action_open_text_list = []
    action_close_start_text_list = []
    action_close_end_text_list = []

    file_name_list = []


    text_map_and_single_text_lines_list = []

    elements = MsTeamsAdaptiveCardElements()

    def create_files_for_presentation(self, file_blocks: list[FileBlock]) -> list[map]:
        file_content_list = []

        for file_block in file_blocks:
            if not self.__its_txt_file(file_block.filename):
                continue
            self.__create_new_keys()
            self.file_name_list.append(file_block.filename)
            file_content_list.append(file_block.contents)

        if len(self.open_key_list) == 0:
            return []

        for index in range(len(self.open_key_list)):
            self.__manage_blocks_for_single_file(index, self.file_name_list[index], file_content_list[index])
        return self.__manage_all_text_to_send()

    def get_text_map_and_single_text_lines_list(self):
        return self.text_map_and_single_text_lines_list

    def __create_new_keys(self):
        self.open_key_list.append(str(uuid.uuid4()))
        self.close_start_key_list.append(str(uuid.uuid4()))
        self.close_end_key_list.append(str(uuid.uuid4()))
        self.text_file_presentaiton_key_list.append(str(uuid.uuid4()))

    def __manage_blocks_for_single_file(self, index, file_name : str, content : bytes):
        open_text_action = self.__action(index, open=True, title='press to open')
        close_text_action = self.__action(index, open =False, title='press to close')

        open_text = self.elements.text_block('***open ' + file_name + '***', isSubtle=False)
        close_start = self.elements.text_block('***close ' + file_name + '***', isSubtle=False)
        close_end = self.elements.text_block('***close ' + file_name + '***', isSubtle=False)

        self.open_text_list.append(open_text)
        self.close_start_text_list.append(close_start)
        self.close_end_text_list.append(close_end)

        self.action_open_text_list.append(open_text_action)
        self.action_close_start_text_list.append(close_text_action)
        self.action_close_end_text_list.append(close_text_action)

        self.text_file_presentaiton_list.append(self.__present_text_file_block(self.text_file_presentaiton_key_list[index], content.decode('utf-8')))

    def __manage_all_text_to_send(self):
        columns_set_list = []

        top_column_list = []
        botom_column_list = []
        for index in range(len(self.open_text_list)):
            width = self.__calc_file_name_width(index)
            
            
            top_column_list.append( self.elements.column(width_number=width, isVisible=True, key=self.open_key_list[index], 
                            items=[self.open_text_list[index]], action= self.action_open_text_list[index]))

            top_column_list.append(  self.elements.column(width_number=width, isVisible=False, key=self.close_start_key_list[index], 
                        items=[self.close_start_text_list[index]], action=self.action_close_start_text_list[index]))

            botom_column_list.append(  self.elements.column(width_number=width, isVisible=False, key=self.close_end_key_list[index], 
                        items=[self.close_end_text_list[index]], action=self.action_close_end_text_list[index]))

        top_column_set = self.elements.column_set(top_column_list)        
        bottom_column_set = self.elements.column_set(botom_column_list)

        list_to_return = [top_column_set]
        list_to_return += self.text_file_presentaiton_list
        list_to_return.append(bottom_column_set)

        return list_to_return
    
    # need to calc the approximate size of the file name + the prefix, otherwise it will spread on the entire line
    def __calc_file_name_width(self, index):
        # taking the max letters so there wont be movement in textblock
        prefix_letters = 'close '
        prefix_letters.replace('','')
        width = 7 * len(prefix_letters + self.file_name_list[index].replace('***', '')) + 40
        return str(width)

    def __action(self, index, open : bool, title : str) -> map:
        visible_elements_map = {False : [], True : []}
        curr_key = self.open_key_list[index]
        for key in self.open_key_list:
            visible = (not open) or (curr_key != key)
            visible_elements_map[visible].append(key)

        curr_key = self.close_start_key_list[index]
        for key in self.close_start_key_list:
            visible = open and (curr_key == key)
            visible_elements_map[visible].append(key)

        curr_key = self.close_end_key_list[index]
        for key in self.close_end_key_list:
            visible = open and (curr_key == key)
            visible_elements_map[visible].append(key)

        curr_key = self.text_file_presentaiton_key_list[index]
        for key in self.text_file_presentaiton_key_list:
            visible = open and (curr_key == key)
            visible_elements_map[visible].append(key)
        visible_elements : list[map] = self.elements.action_toggle_target_elements(
            visible_keys= visible_elements_map[True], invisible_keys =visible_elements_map[False])

        return self.elements.action (title=title, target_elements=visible_elements)

    # there is a limit to the number of letters you can write - dont know what it is !!!
    # /t doesn't work so we need to simulate spaces (which are trimmed so we use '. . . ')
    def __present_text_file_block(self, key : str, text : str):
        text_lines_list = []
        new_text = text.replace('\t', '. . . ')

        for line in new_text.split('\n'):
            text_lines_list.append(line + '\n\n')

        # will be completed later
        text_block = self.elements.text_block('', wrap=True, weight='bolder', isVisible=True)
        self.text_map_and_single_text_lines_list.append([text_block, text_lines_list])
        return self.elements.container(key=key, items=[text_block])

    def __its_txt_file(self, file_name: str):
        txt_prefix_list = ['.txt', '.json', '.yaml']
        if file_name[-4:] in txt_prefix_list:
            return True
        return False