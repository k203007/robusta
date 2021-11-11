from ...core.reporting.blocks import *
from .msteams_adaptive_card_files_image import MsTeamsAdaptiveCardFilesImage
from .msteams_adaptive_card_files_text import MsTeamsAdaptiveCardFilesText

# TODO: always return Element class (everything inherits from element)
class MsTeamsAdaptiveCardFiles:

    def __init__(self):
        self.files_keys_list = []
        self.text_files = MsTeamsAdaptiveCardFilesText()
        self.image_files = MsTeamsAdaptiveCardFilesImage()

    # TODO: - return only one function not 3 
    def upload_files(self, file_blocks: list[FileBlock]) -> list[map]:
        image_section_map : map = self.image_files.create_files_for_presentation(file_blocks)
        text_files_section_list = self.text_files.create_files_for_presentation(file_blocks)

        if image_section_map:
            image_section_map = [image_section_map]
        else:
            image_section_map = []
        return text_files_section_list  + image_section_map

    # TODO - make this shorter and more clear
    def get_text_map_and_single_text_lines_list__for_text_files(self):
        return self.text_files.get_text_map_and_single_text_lines_list()

    def get_url_map_list(self):
        return self.image_files.get_url_map_list()        