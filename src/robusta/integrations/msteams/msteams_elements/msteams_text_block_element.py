from .msteams_base_element import MsTeamsBaseElement
from ..msteams_mark_down_fix_url import MsTeamsMarkDOwnFixUrl

class MsTeamsTextBlockElement(MsTeamsBaseElement):
    def __init__(self, text : str, isSubtle : bool = None, wrap: bool = None, weight: str = None, isVisible : bool = True, 
                separator : bool = False, font_size : str = 'medium', horizontalAlignment : str = "left") -> MsTeamsBaseElement:

        curr_map : map = self.__text_block(text, isSubtle, wrap, weight, isVisible, 
                separator, font_size, horizontalAlignment) 
        super().__init__(curr_map)
    

    def __text_block(self, text : str, isSubtle : bool = None, wrap: bool = None, weight: str = None, isVisible : bool = True, 
                separator : bool = False, font_size : str = 'medium', horizontalAlignment : str = "left"):
        self.block = {}
        self.block[self.__type] = "TextBlock" 
        self.block["text"] = MsTeamsMarkDOwnFixUrl().fix_text(text)
        self.block["size"] = font_size
        self.block["isVisible"] = isVisible        
        self.block["separator"] = separator
        self.block["horizontalAlignment"] = horizontalAlignment

        if isSubtle is not None:
            self.block["isSubtle"] = isSubtle 
        self.block["wrap"] = True
        if weight is not None:
            self.block["weight"] = weight 

    def get_text_from_block(self) -> str:
        return self.block["text"]

    def set_text_from_block(self, text : str):
        self.block["text"] = text


