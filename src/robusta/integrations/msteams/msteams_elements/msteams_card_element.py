from .msteams_base_element import MsTeamsBaseElement

class MsTeamsCardElement(MsTeamsBaseElement):
    def __init__(self, body: list[MsTeamsBaseElement]) -> None:
        content = {}
        content["$schema"] = "http://adaptivecards.io/schemas/adaptive-card.json"
        content["type"] = "AdaptiveCard"
        content["version"] = "1.2"
        content["msTeams"] = {"width": "full"}
        content["body"] = self.__to_map_list(body)

        atachment_map = {}
        atachment_map["contentType"] = "application/vnd.microsoft.card.adaptive"
        atachment_map["contentUrl"] = None
        atachment_map["content"] = content
        
        block = {}
        block["type"] = "message"
        block["attachments"] = [atachment_map]

        super().__init__(block)
    
    def __to_map_list(self, elements : list[MsTeamsBaseElement]):
        curr_list = []
        for e in elements:
            curr_list = curr_list + e.get_map_values()
        return curr_list
