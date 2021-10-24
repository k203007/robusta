
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

    def __get_column_for_separator(self, separator: bool):
        separator_text = 'false'
        if separator:
            separator_text = 'true'
        block = '''
            {{"type":"TextBlock","isSubtle":true,"text":" ",}},
            {{"type":"TextBlock","isSubtle":true,"text":" ","separator": {0} }},

        '''
        return block.format(separator_text)

    def __separator(self, columns_str: str):
        block = '''
        {{
         "type":"ColumnSet",
         "columns":[
            {{
                "type":"Column",
                "width":"stretch",
                "items":[
                    {0}
                ],
            }},
         ]
        }},
        '''
        return block.format(columns_str)        

    def get_section_separator(self):
        return self.__separator(self.__get_column_for_separator(True))

    def get_sub_section_separator(self):
        return self.__separator(self.__get_column_for_separator(False) + 
            self.__get_column_for_separator(False) + 
            self.__get_column_for_separator(True))
