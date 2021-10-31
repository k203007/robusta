
class MsTeamsAdaptiveCardElements:
    __type = 'type'

    def image_set(self, images_list : list[map]) -> map:
        block = {}
        block[self.__type] =  "ImageSet"
        block["imageSize"] = "large"
        block["images"]=  images_list
        return block

    def column_set(self, columns_list : list[map]) -> map:
        block = {}
        block[self.__type] =  "ColumnSet"
        block["columns"]=  columns_list
        return block

    def action(self, title : str, target_elements : list[map]):
        block = {}
        block["selectAction"] = {}
        block["selectAction"]["type"] = "Action.ToggleVisibility"
        block["selectAction"]["title"] = title
        block["selectAction"]["targetElements"] = target_elements

        return block

    def get_text_from_block(self, block : map) -> str:
        return block["text"]

    def set_text_from_block(self, block : map, text : str):
        block["text"] = text

    def get_image_url_size(self, image_map : map) -> int:
        return len(image_map["url"])

    def present_image(self, url : str) -> map:
        block = {}
        block[self.__type] = "Image"
        block["url"] = url
        block["msTeams"] = { "allowExpand": True }    
        return block      

    def text_block(self, text : str, isSubtle : bool = None, wrap: bool = None, weight: str = None, isVisible : bool = True, 
                separator : bool = False, font_size : str = 'medium', horizontalAlignment : str = "left"):
        block = {}
        block[self.__type] = "TextBlock" 
        block["text"] = text
        block["size"] = font_size
        block["isVisible"] = isVisible        
        block["separator"] = separator
        block["horizontalAlignment"] = horizontalAlignment

        if isSubtle is not None:
            block["isSubtle"] = isSubtle 
        if wrap is not None:
            block["wrap"] = wrap 
        if weight is not None:
            block["weight"] = weight 
        return block

    def container(self, key : str = None, items : list[map] = []):
        block = {}
        block[self.__type] = "Container"
        block["style"] = "accent"
        block["isVisible"] = False
        if key is not None:
            block["id"] = key
        block["bleed"] = False
        block["items"] = items
        return block

    def column(self, width_number: int = None, width_strech : bool = None, isVisible : bool = True, 
                key : str = None, items : list[map] = [], action : map = {}):
        block = {}
        block[self.__type] = "Column"
        if width_number is not None:
            block["width"] = str(width_number) + "px"
        if width_strech is not None:
            if width_strech:
                block["width"] = "stretch"
            else:
                block["width"] = "auto"

        block["isVisible"] = isVisible
        block["isVisible"] = isVisible
        if key is not None:
            block["id"] = key
        block["items"] = items
        block = block | action
        return block

    def action_toggle_target_elements(self, visible_keys : list[str], invisible_keys : list[str]) -> list[map]:
        actions = []

        actions = self.__set_toggle_action(visible_keys, True)
        actions += self.__set_toggle_action(invisible_keys, False)
        
        return actions

    def __set_toggle_action(self, keys : list[str], visible : bool):
        block_list = []
        for key in keys:
            block = {}
            block["elementId"] = key
            block["isVisible"] = visible
            block_list.append(block)
        return block_list
    
    def card(self, body : list[map]):
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

        content = {}
        content["$schema"] = "http://adaptivecards.io/schemas/adaptive-card.json"
        content["type"] = "AdaptiveCard"
        content["version"] = "1.2"
        content["msTeams"] = {"width": "full"}
        content["body"] = body

        atachment_map = {}
        atachment_map["contentType"] = "application/vnd.microsoft.card.adaptive"
        atachment_map["contentUrl"] = None
        atachment_map["content"] = content
        
        block = {}
        block["type"] = "message"
        block["attachments"] = [atachment_map]

        return block
