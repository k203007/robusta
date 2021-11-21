from .msteams_base_element import MsTeamsBaseElement

class MsTeamsActionElement(MsTeamsBaseElement):
    def __init__(self, title : str, visible_keys: list[str], invisible_keys: list[str]) -> None:
        self.column_list = []
        super().__init__(self.__action(title, visible_keys, invisible_keys))

    def __action(self, title : str, visible_keys: list[str], invisible_keys: list[str]):
        block = {}
        block["selectAction"] = {}
        block["selectAction"]["type"] = "Action.ToggleVisibility"
        block["selectAction"]["title"] = title
        block["selectAction"]["targetElements"] = self.__action_toggle_target_elements(visible_keys, invisible_keys)

        return block

    def __action_toggle_target_elements(self, visible_keys : list[str], invisible_keys : list[str]) -> list[map]:
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