
from enum import Enum


class AdaptiveCardFontSize(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    EXTRA_LARGE = "extraLarge"


class MsTeamsAdaptiveCard:

    def setBody(self, body : str):
        __BODY =  """{
                        "type":"message",
                        "attachments":[
                        {
                            "contentType":"application/vnd.microsoft.card.adaptive",
                            "contentUrl":null,
                            "content":{
                                "$schema":"http://adaptivecards.io/schemas/adaptive-card.json",
                                "type":"AdaptiveCard",
                                "version":"1.2",
                                "body":[
                                    {0}  
                                ]
                            }
                        }
                    }"""

        return body.format(body)


    def set_text_block(self, text : str, font_size : AdaptiveCardFontSize):
        block = ''' {
                "type": "TextBlock",
                "text": "{0}",
                "size": "{1}"
                } '''
        return block.format(text, font_size.value)

    def set_image(self):
        pass