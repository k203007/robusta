import tempfile
import base64
import os
from uuid import uuid1
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image

from .msteams_adaptive_card_elements  import MsTeamsAdaptiveCardElements
from ...core.reporting.blocks import *


class MsTeamsAdaptiveCardFilesImage:

    elements = MsTeamsAdaptiveCardElements()
    url_map_list = []

    def create_files_for_presentation(self, file_blocks: list[FileBlock]) -> map:
        images_list = []        
        for file_block in file_blocks:
            if not self.__file_is_image(file_block.filename):
                continue
            data_url = self.__convert_bytes_to_base_64_url(file_block.filename, file_block.contents)
            image_map = self.elements.present_image(data_url)
            self.url_map_list.append(image_map)
            images_list.append(self.elements.present_image(data_url))
        if len(images_list) == 0:
            return {}
        return self.elements.image_set(images_list)

    def get_url_map_list(self):
        return self.url_map_list

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