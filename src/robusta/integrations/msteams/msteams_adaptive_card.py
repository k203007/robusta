
from enum import Enum
from typing import Awaitable


class CardElements(Enum):
    TEXT = 'text',
    IMAGE = 'image',
    SECTION = 'section'
    



class AdaptiveCardFontSize(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    EXTRA_LARGE = "extraLarge"


class MsTeamsAdaptiveCard:

    curr_card = ''

    def get_msg_to_send(self, body: str):
        __BODY =  """{{
                        "type":"message",
                        "attachments":[
                        {{
                            "contentType":"application/vnd.microsoft.card.adaptive",
                            "contentUrl":null,
                            "content":{{
                                "$schema":"http://adaptivecards.io/schemas/adaptive-card.json",
                                "type":"AdaptiveCard",
                                "version":"1.2",
                                "msTeams": {{ "width": "full" }},
                                "body":[
                                    {0}  
                                ]
                            }}
                        }}
                        ]
                    }}"""

        return __BODY.format(self.curr_card + body)

    def set_text_block(self, text : str, font_size : AdaptiveCardFontSize):
        block = ''' {{
                "type": "TextBlock",
                "text": "{0}",
                "size": "{1}"
                }}, '''
        self.curr_card += block.format(text, font_size.value)

    def get_text_block(self, text : str, font_size : AdaptiveCardFontSize):
        block = ''' {{
                "type": "TextBlock",
                "text": "{0}",
                "size": "{1}"
                }}, '''
        return block.format(text, font_size.value)



    def get_section_separator(self):
        block = '''
            {{
        "type": "Container",
        "minHeight": "50px",
        "style": "default",
        "items": []
        }},'''
        return block

    def get_image_thumbnail_block_list(self, block_str_list : list[str]):
        block = '''{{
        "type": "ImageSet",
        "imageSize": "large",
        "images": [{0}]
        }},'''
        s = ''
        for str_block in block_str_list:
            s += str_block
        return block.format(s)

    def get_image_thumbnail(self, data_url):
        block = '''{{
            "type": "Image",
            "url": "{0}"
        }},'''
        return block.format(data_url)

    def get_image(self, data_url):
        block = '''{{
            "type": "Image",
            "url": "{0}"
        }},'''
        return block.format(data_url)