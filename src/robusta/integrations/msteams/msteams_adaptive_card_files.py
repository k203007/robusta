from ...core.reporting.blocks import *
from .msteams_adaptive_card_files_image import MsTeamsAdaptiveCardFilesImage
from .msteams_adaptive_card_files_text import MsTeamsAdaptiveCardFilesText

class MsTeamsAdaptiveCardFiles:

    files_keys_list = []

    def upload_files(self, file_blocks: list[FileBlock]):
        image_section_str = MsTeamsAdaptiveCardFilesImage().create_files_for_presentation(file_blocks)
        text_files_section_str = MsTeamsAdaptiveCardFilesText().create_files_for_presentation(file_blocks)

        return image_section_str + text_files_section_str

