
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

    def get_text_block(self, text : str, font_size : AdaptiveCardFontSize):
        block = ''' {{
                "type": "TextBlock",
                "text": "{0}",
                "size": "{1}"
                }}, '''
        return block.format(text, font_size.value)

    def get_section_separator(self):
        block = '''
        {{"type":"ColumnSet","columns":[
            {{
                "type":"Column","width":"stretch","items":[
                    {{"type":"TextBlock","text":" ",}},
                    {{"type":"TextBlock","text":" ","separator": true }},
                ],
            }},
         ]
        }},
        '''
        return block.format()

    def get_sub_section_separator(self):
        line = '____________________________________'
        space_block = '{{"type": "TextBlock","text": " ","size": "small",}},'
        line_block = '{{"type": "TextBlock","text": "{0}","horizontalAlignment": "center","color": "accent","size": "small",}},'
        return space_block.format() * 1 + line_block.format(line) + space_block.format() * 2
