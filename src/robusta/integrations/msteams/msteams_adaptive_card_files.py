from ...core.reporting.blocks import *


class MsTeamsAdaptiveCardFiles:

    files_keys_list = []

    def upload_files(self, file_blocks: list[FileBlock]):
        files = ''
        str_thumbnail_blocks_list = []
        
        self.__set_files_key_list()
        index = 0
        for file_block in file_blocks:
            if self.__file_is_image(file_block.filename):
                data_url = self.__convert_bytes_to_base_64_url(file_block.filename, file_block.contents)                
                key = self.files_keys_list[index]
                files += self.__get_image(data_url, key)
                str_thumbnail_blocks_list.append(self.__get_image_thumbnail(data_url, key))
                index += 1
        self.current_body_string += self.__get_image_thumbnail_block_list(str_thumbnail_blocks_list)
        self.current_body_string += files

    def __set_files_key_list(self, file_blocks):
        for file_block in file_blocks:
            self.files_keys_list.append(str(uuid.uuid4()))

    def __get_image_thumbnail_block_list(self, block_str_list : list[str]):
        block = '''{{
        "type": "ImageSet",
        "imageSize": "large",
        "images": [{0}]
        }},'''
        s = ''
        for str_block in block_str_list:
            s += str_block
        return block.format(s)

    def __set_action(self, key_to_make_visible: str) -> str:
        block = '''
            "selectAction": {{
                    "type": "Action.ToggleVisibility",
                    "title": "cool link",
                    "targetElements": [{0}]
            }},
        '''
        action_toggle_str = ''
        for key in self.files_keys_list:
            visible = key_to_make_visible == key
            action_toggle_str += self.__single_action_toggle(key, visible)
        block.format(action_toggle_str)

    def __single_action_toggle(self, key : str, visible : bool):
        block = '''{{
          "elementId": {0},
          "isVisible": {1}
        }},'''
        visible_txt = 'false'
        if visible:
            visible_txt = 'true'
        return block.format(key, visible_txt)

    def __get_image_thumbnail(self, data_url : str, image_key : str):
        block = '''{{
            "type": "Image",
            "url": "{0}",
            {1}           
        }},'''
        action : str = self.__set_action(image_key)
        return block.format(data_url, action)

    def __get_image(self, data_url: str, key: str):
        block = '''{{
            "type": "Image",
            "url": "{0}",
            "isVisible": false,
            "id": "{1}",
        }},'''
        return block.format(data_url, key)
