from ...core.reporting.blocks import *
from .msteams_adaptive_card_files_image import MsTeamsAdaptiveCardFilesImage
from .msteams_adaptive_card_files_text import MsTeamsAdaptiveCardFilesText

class MsTeamsAdaptiveCardFiles:

    files_keys_list = []

    def upload_files(self, file_blocks: list[FileBlock]) -> list[map]:
        image_section_map : map = MsTeamsAdaptiveCardFilesImage().create_files_for_presentation(file_blocks)
        text_files_section_list = MsTeamsAdaptiveCardFilesText().create_files_for_presentation(file_blocks)

        return text_files_section_list  + [image_section_map]

