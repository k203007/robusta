import tempfile
import base64
import os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image

from .msteams_colum_element import MsTeamsColumnElement
from .msteams_text_block_element import MsTeamsTextBlockElement
from .msteams_base_element import MsTeamsBaseElement

class MsTeamsTableElement(MsTeamsBaseElement):
    def __init__(self, header_list: list[str], rows: list[list[str]]):
        column_element = self.__create_table(header_list, rows)
        super().__init__(column_element.get_map_value())

    def __create_table(self, header_list: list[str], rows: list[list[str]]) -> MsTeamsColumnElement:

        all_columns = []
        column_element = MsTeamsColumnElement()
        for index in range(len(header_list)):
            single_column = []
            single_column.append(MsTeamsTextBlockElement(text=header_list[index], weight="bolder"))
            single_column = single_column + self.__create_single_column_list(rows_list=rows, index=index)
            column_element.single_column(items = single_column, width_strech = bool)

        return column_element

    def __create_single_column_list(self, rows_list : list[list[str]], index : int) -> list[map]:
        first_row = True
        column = []
        for row_list in rows_list:            
            column.append(MsTeamsTextBlockElement(text=row_list[index], separator=first_row))
            first_row = False
        return column
