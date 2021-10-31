from ...core.reporting.blocks import *
from .msteams_adaptive_card_files_image import MsTeamsAdaptiveCardFilesImage
from .msteams_adaptive_card_files_text import MsTeamsAdaptiveCardFilesText

class MsTeamsAdaptiveCardFiles:

    files_keys_list = []
    text_files = MsTeamsAdaptiveCardFilesText()
    image_files = MsTeamsAdaptiveCardFilesImage()
    def upload_files(self, file_blocks: list[FileBlock]) -> list[map]:
        image_section_map : map = self.image_files.create_files_for_presentation(file_blocks)
        text_files_section_list = self.text_files.create_files_for_presentation(file_blocks)

        return text_files_section_list  + [image_section_map]

    def get_text_map_and_single_text_lines_list__for_text_files(self):
        return self.text_files.get_text_map_and_single_text_lines_list()

    def get_url_map_list(self):
        return self.image_files.get_url_map_list()        