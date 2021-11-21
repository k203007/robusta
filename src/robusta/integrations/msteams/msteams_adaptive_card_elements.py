from .msteams_mark_down_fix_url import MsTeamsMarkDOwnFixUrl

# TODO: class for each element the inherits from MAP
# TODO: create a monsterous readme with all the link to websites I found
class MsTeamsAdaptiveCardElements:
    __type = 'type'

    def action(self, title : str, target_elements : list[map]):
        block = {}
        block["selectAction"] = {}
        block["selectAction"]["type"] = "Action.ToggleVisibility"
        block["selectAction"]["title"] = title
        block["selectAction"]["targetElements"] = target_elements

        return block

    def get_image_url_size(self, image_map : map) -> int:
        return len(image_map["url"])

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