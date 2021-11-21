from .msteams_base_element import MsTeamsBaseElement

class MsTeamsImagesElement(MsTeamsBaseElement):
    def __init__(self, url_list : list[str]) -> None:        
        map_list : list = []
        self.images_len_in_bytes = 0
        for url in url_list:
            map_list.append(self.__single_image(url))

        super().__init__(self.__image_set(map_list))

    def get_images_len_in_bytes(self):
        return self.images_len_in_bytes

    def __image_set(self, images_list : list[map]) -> map:
        block = {}
        block['type'] =  "ImageSet"
        block["imageSize"] = "large"
        block["images"]=  images_list
        return block

    def __single_image(self, url : str) -> map:
        self.images_len_in_bytes += len(url)
        block = {}
        block['type'] = "Image"
        block["url"] = url
        block["msTeams"] = { "allowExpand": True }    
        return block      

