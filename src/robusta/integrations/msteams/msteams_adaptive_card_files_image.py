import tempfile
import base64
import os
from uuid import uuid1
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image
from ...core.reporting.blocks import *


class MsTeamsAdaptiveCardFilesImage:

    files_keys_list = []

    def create_files_for_presentation(self, file_blocks: list[FileBlock]):
        files = ''
        str_thumbnail_blocks_list = []
        
        self.__set_files_key_list(file_blocks)
        index = 0
        for file_block in file_blocks:
            if not self.__file_is_image(file_block.filename):
                continue
            data_url = self.__convert_bytes_to_base_64_url(file_block.filename, file_block.contents)                
#                data_url = 'aaa'
            key = self.files_keys_list[index]
            files += self.__get_image(data_url, key)
            str_thumbnail_blocks_list.append(self.__get_image_thumbnail(data_url, key))
            index += 1

        image_section_str = self.__get_image_thumbnail_block_list(str_thumbnail_blocks_list)
        image_section_str += files
        return image_section_str

    def __get_tmp_file_path(self):
        tmp_dir_path = tempfile.gettempdir() 
        return tmp_dir_path + '/' + str(uuid.uuid1())

    def __file_is_jpg(self, file_name: str):
        return file_name.endswith('.jpg')
    def __file_is_png(self, file_name: str):
        return file_name.endswith('.png')
    def __file_is_svg(self, file_name: str):
        return file_name.endswith('.svg')
    
    def __file_is_image(self, file_name: str):
        return self.__file_is_jpg(file_name) \
            or self.__file_is_png(file_name) \
            or self.__file_is_svg(file_name) \

    def __convert_bytes_to_base_64_url(self, file_name: str, bytes: bytes):
        if self.__file_is_jpg(file_name):
            return self.__jpg_convert_bytes_to_base_64_url(bytes)
        if self.__file_is_png(file_name):
            return self.__png_convert_bytes_to_base_64_url(bytes)
        return self.__svg_convert_bytes_to_jpg(bytes)

    def __jpg_convert_bytes_to_base_64_url(self, bytes : bytes):
        b64_string = base64.b64encode(bytes).decode("utf-8") 
        return 'data:image/jpeg;base64,{0}'.format(b64_string)

    #msteams cant read parsing of url to 'data:image/png;base64,...
    def __png_convert_bytes_to_base_64_url(self, bytes : bytes):
        png_file_path = self.__get_tmp_file_path() + '.png'
        jpg_file_path = self.__get_tmp_file_path() + '.jpg'
        with open(png_file_path, 'wb') as f:
            f.write(bytes)

        im = Image.open(png_file_path)
        rgb_im = im.convert('RGB')
        rgb_im.save(jpg_file_path)
        with open(jpg_file_path, 'rb') as f:
            jpg_bytes = f.read()

        os.remove(png_file_path)
        os.remove(jpg_file_path)

        return self.__jpg_convert_bytes_to_base_64_url(jpg_bytes)

    #msteams cant read parsing of url to svg image
    def __svg_convert_bytes_to_jpg(self, bytes : bytes):
        svg_file_path = self.__get_tmp_file_path()
        with open(svg_file_path, 'wb') as f:
            f.write(bytes)

        drawing = svg2rlg(svg_file_path)
        jpg_file_path = self.__get_tmp_file_path()

        renderPM.drawToFile(drawing, jpg_file_path, fmt="JPG")
        with open(jpg_file_path, 'rb') as f:
            jpg_bytes = f.read()

        os.remove(svg_file_path)
        os.remove(jpg_file_path)

        return self.__jpg_convert_bytes_to_base_64_url(jpg_bytes)


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
        toggle_block = '''
            "selectAction": {{
                    "type": "Action.ToggleVisibility",
                    "title": "cool link",
                    "targetElements": [{0}]
            }},
        '''

        block = '''
                    "msTeams": {{ "allowExpand": true }},
        '''
        action_toggle_str = ''
        for key in self.files_keys_list:
            visible = key_to_make_visible == key
            action_toggle_str += self.__single_action_toggle(key, visible)
        #return block.format(action_toggle_str)
        return block.format()

    def __single_action_toggle(self, key : str, visible : bool):
        block = '''{{
          "elementId": "{0}",
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
