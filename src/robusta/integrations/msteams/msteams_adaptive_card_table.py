import tempfile
import base64
import os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image

from .msteams_adaptive_card_elements import MsTeamsAdaptiveCardElements
from ...core.reporting.blocks import *

# TODO: change to TABLE element - try put everything in parameters in init 
class MsTeamsAdaptiveCardTable:
    def __init__(self):
        self.elements = MsTeamsAdaptiveCardElements()

    def create_table(self, header_list: list[str], rows: list[list[str]]) -> map:
        all_columns = []
        for index in range(len(header_list)):
            column = []
            column.append(self.elements.text_block(text=header_list[index], weight="bolder"))

            column = column + self.create_column(rows_list=rows, index=index)

            all_columns.append(self.elements.column(items= column, width_strech=False))
        return self.elements.column_set(all_columns)

    def create_column(self, rows_list : list[list[str]], index : int) -> list[map]:
        first_row = True
        column = []
        for row_list in rows_list:            
            column.append(self.elements.text_block(text=row_list[index], separator=first_row))
            first_row = False
        return column
