import tempfile
import base64
import os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image

from .msteams_colum_element import MsTeamsColumnElement
from .msteams_text_block_element import MsTeamsTextBlockElement

class MsTeamsTableElement:
    def __init__(self, header_list: list[str], rows: list[list[str]]):
        super().__init__(self.__create_table(header_list, rows))

    def __create_table(self, header_list: list[str], rows: list[list[str]]) -> map:
        all_columns = []
        for index in range(len(header_list)):
            single_column = []
            single_column.append(MsTeamsTextBlockElement(text=header_list[index], weight="bolder"))
            single_column = single_column + self.__create_single_column_list(rows_list=rows, index=index)
            all_columns.append(all_columns)
        
        column_element = MsTeamsColumnElement()
        column_element.column_list(items = all_columns, width_strech = bool)
        return MsTeamsColumnElement(all_columns)

    def __create_single_column_list(self, rows_list : list[list[str]], index : int) -> list[map]:
        first_row = True
        column = []
        for row_list in rows_list:            
            column.append(MsTeamsTextBlockElement(text=row_list[index], separator=first_row))
            first_row = False
        return column
