from .msteams_base_element import MsTeamsBaseElement

class MsTeamsColumnElement(MsTeamsBaseElement):
    
    def __init__(self) -> None:
        self.column_list = []
        super().__init__(self.__column_set())
        pass

    def __column_set(self) -> map:
        block = {}
        block[self.__type] =  "ColumnSet"
        block["columns"] = self.column_list
        return block

    def single_column(self, width_strech : bool = False, isVisible : bool = True, 
                key : str = None, items : list[map] = [], action : map = {}):
        block = {}
        block[self.__type] = "Column"
        if width_strech is not None:
            if width_strech:
                block["width"] = "stretch"
            else:
                block["width"] = "auto"

        block["isVisible"] = isVisible
        if key is not None:
            block["id"] = key
        block["items"] = items
        block = block | action

        self.column_list.append(block)
