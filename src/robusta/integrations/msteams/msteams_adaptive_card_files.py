from ...core.reporting.blocks import *
from .msteams_adaptive_card_files_image import MsTeamsAdaptiveCardFilesImage
from .msteams_adaptive_card_files_text import MsTeamsAdaptiveCardFilesText
from .msteams_elements.msteams_base_element import MsTeamsBaseElement

# TODO: always return Element class (everything inherits from element)
class MsTeamsAdaptiveCardFiles(MsTeamsBaseElement):

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

    # return the list of text containers with the list of lines, so later ater 
    # calculating the length of bytes left in the message, we can put the 
    # lines evenly in each text container so we dont excced the msg length
    def get_text_files_containers_list(self):
        return self.text_files.get_text_files_containers_list()