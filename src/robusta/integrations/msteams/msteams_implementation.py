import json
import logging
import tempfile
import requests
import base64

import tempfile
import uuid

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from .msteams_adaptive_card import AdaptiveCardFontSize,MsTeamsAdaptiveCard
from ...core.model.events import *
from ...core.reporting.blocks import *
from ...core.reporting.utils import add_pngs_for_all_svgs
from ...core.reporting.callbacks import PlaybookCallbackRequest
from ...core.reporting.consts import SlackAnnotations
from ...core.model.env_vars import TARGET_ID

ACTION_TRIGGER_PLAYBOOK = "trigger_playbook"
MsTeamsBlock = Dict[str, Any]

class MsTeamsImplementation:
    current_body_string = ''
    current_section_string = ''
    msteams_hookurl = ''


    def __init__(self, msteams_hookurl: str, title: str, description: str):
        try:
            self.msteams_hookurl = msteams_hookurl
            self.myTeamsMessage = MsTeamsAdaptiveCard()
            self.myTeamsMessage.set_text_block(title, AdaptiveCardFontSize.EXTRA_LARGE)
            if description is not None:
                self.myTeamsMessage.set_text_block(description, AdaptiveCardFontSize.MEDIUM)
        except Exception as e:
            logging.error(f"Error creating MsTeamsAdaptiveCard: {e}")
            raise e

    def __get_tmp_file_path():
        tmp_dir_path = tempfile.gettempdir() 
        return tmp_dir_path + str(uuid.uuid1())


    def new_card_section(self):
        # write previous section
        self.__write_section_to_card()

    def __write_section_to_card(self):
        if self.current_section_string == '':
            return
        #self.current_body_string += self.myTeamsMessage.get_section_separator()
        self.current_body_string += self.current_section_string
        self.current_section_string = ''

    def __file_is_image(file_name: str):
        if (file_name.endswith('.jpg')):
            return True
        if (file_name.endswith('.png')):
            return True
        if (file_name.endswith('.svg')):
            return True
        return False

    def __jpg_convert_bytes_to_base_64_url(bytes : bytes):
        b64_string = base64.b64encode(bytes)
        return 'data:image/jpeg;base64,{0}'.format(b64_string)

    def __png_convert_bytes_to_base_64_url(bytes : bytes):
        b64_string = base64.b64encode(bytes)
        return 'data:image/png;base64,{0}'.format(b64_string)

    def __svg_convert_bytes_to_jpg(self, bytes : bytes):
        svg_file_path = self.__get_tmp_file_path()
        with open(svg_file_path, 'wb') as f:
            f.write(bytes)

        drawing = svg2rlg(svg_file_path)
        jpg_file_path = self.__get_tmp_file_path()

        renderPM.drawToFile(drawing, jpg_file_path, fmt="JPG")
        with open(jpg_file_path, 'rb') as f:
            f.read(bytes)




    def upload_files(self, file_blocks: list[FileBlock]):        
        for file_block in file_blocks:
            file_block.filename
            pass

    def send(self):
        try:
            self.__write_section_to_card()
            response = requests.post(self.msteams_hookurl, data = self.myTeamsMessage.get_msg_to_send(self.current_body_string))
            print(response)
        except Exception as e:
            logging.error(f"error sending message to msteams\ne={e}\n")
        

    def diff(self, block: KubernetesDiffBlock):
        data = ''
        for d in block.diffs:
            data = f"*{d.formatted_path}*: {d.other_value} :arrow_right: {d.value}"
            data += '\n'
        self.current_section_string += self.__new_line_replacer(data + '\n\n')


    def markdown_block(self, block: BaseBlock):
        if not block.text:
            return
        text = self.__apply_length_limit(block.text) + self.__new_line_replacer('\n\n')
        self.current_section_string += self.myTeamsMessage.get_text_block(text, AdaptiveCardFontSize.MEDIUM)
        print(self.myTeamsMessage.get_text_block(text, AdaptiveCardFontSize.MEDIUM))

    def divider_block(self, block: BaseBlock):
        self.current_section_string += self.__new_line_replacer('\n\n')

    def header_block(self, block: BaseBlock):
        current_header_string = self.__apply_length_limit(block.text, 150) + self.__new_line_replacer('\n\n')
        self.current_section_string += self.myTeamsMessage.get_text_block(current_header_string, AdaptiveCardFontSize.EXTRA_LARGE)

    def get_action_block_for_choices(self, choices: Dict[str, Callable] = None, context=""):
        if choices is None:
          return
        '''
        buttons = []
        for (i, (text, callback)) in enumerate(choices.items()):
            buttons.append(
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": text,
                    },
                    "style": "primary",
                    "action_id": f"{ACTION_TRIGGER_PLAYBOOK}_{i}",
                    "value": PlaybookCallbackRequest.create_for_func(
                        callback, context, text
                    ).json(),
                }
            )

        return [{"type": "actions", "elements": buttons}]
        '''

    def __apply_length_limit(self, msg: str, max_length: int = 3000):
        if len(msg) <= max_length:
            return msg
        truncator = "..."
        return self.__new_line_replacer(msg[: max_length - len(truncator)] + truncator)

    def __new_line_replacer(self, text : str):
        return text

