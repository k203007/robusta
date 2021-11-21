
class MsTeamsBaseElement:

    def __init__(self, map_value : map) -> None:
        self.map_value_list = []
        self.map_value_list.append(map_value)

    def add_map_value(self, map_value : map) -> None:
        self.map_value_list.append(map_value)

    def get_map_values(self) -> list[map]:
        return self.map_value_list