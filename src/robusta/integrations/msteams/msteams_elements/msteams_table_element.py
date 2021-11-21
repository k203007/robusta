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
            column = []
            column.append(MsTeamsTextBlockElement(text=header_list[index], weight="bolder"))
            column = column + self.__create_column(rows_list=rows, index=index)
            all_columns.append(self.elements.column(items= column, width_strech=False))

        return MsTeamsColumnElement(all_columns)

    def __create_column(self, rows_list : list[list[str]], index : int) -> list[map]:
        first_row = True
        column = []
        for row_list in rows_list:            
            column.append(MsTeamsTextBlockElement(text=row_list[index], separator=first_row))
            first_row = False
        return column
