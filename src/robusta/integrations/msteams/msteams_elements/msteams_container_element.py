from .msteams_base_element import MsTeamsBaseElement

class MsTeamsContainerElement(MsTeamsBaseElement):
    
    def __init__(self, elements: list[MsTeamsBaseElement]) -> None:
        self.column_list = []
        super().__init__(self.__container(elements))

    def __container(self, key : str = None, elements : list[MsTeamsBaseElement] = []):
        block = {}
        block['type'] = "Container"
        block["style"] = "accent"
        block["isVisible"] = False
        if key is not None:
            block["id"] = key
        block["bleed"] = False
        block["items"] = self.__get_map_list(elements)
        return block

    def __get_map_list(self, elements: list[MsTeamsBaseElement]):
        map_list = []
        for e in elements:
            map_list.append(e.get_map_value)
        return map_list
