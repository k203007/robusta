from .msteams_base_element import MsTeamsBaseElement
from .msteams_action_element import MsTeamsActionElement

class MsTeamsColumnElement(MsTeamsBaseElement):
    
    def __init__(self) -> None:
        self.column_list = []
        super().__init__(self.__column_set())

    def __column_set(self) -> map:
        block = {}
        block['type'] =  "ColumnSet"
        block["columns"] = self.column_list
        return block

    def single_column(self, width_strech : bool = False, isVisible : bool = True, 
                key : str = None, items : list[map] = [], action : MsTeamsActionElement = {}):
        block = {}
        block['type'] = "Column"
        if width_strech is not None:
            if width_strech:
                block["width"] = "stretch"
            else:
                block["width"] = "auto"

        block["isVisible"] = isVisible
        if key is not None:
            block["id"] = key
        block["items"] = self.__to_map_list(items)
        block = block | action

        self.column_list.append(block)

    def __to_map_list(self, elements : list[MsTeamsBaseElement]):
        curr_list = []
        for e in elements:
            curr_list.append(e.get_map_value())
        return curr_list    