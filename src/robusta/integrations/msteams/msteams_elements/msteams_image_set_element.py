from .msteams_base_element import MsTeamsBaseElement

class MsTeamsImageSetElement(MsTeamsBaseElement):
    def __init__(self, url_list : list[str]) -> None:
        
        map_list : list = []
        for url in url_list:
            map_list.append(self.__single_image(url))

        super().__init__(self.__image_set(map_list))


    def __image_set(self, images_list : list[map]) -> map:
        block = {}
        block['type'] =  "ImageSet"
        block["imageSize"] = "large"
        block["images"]=  images_list
        return block

    def __single_image(self, url : str) -> map:
        block = {}
        block['type'] = "Image"
        block["url"] = url
        block["msTeams"] = { "allowExpand": True }    
        return block      

