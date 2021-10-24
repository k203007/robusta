import tempfile
import base64
import os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image
from ...core.reporting.blocks import *

class MsTeamsAdaptiveCardTable:

    def create_table(self, columns_weight_strech : list[bool], header_list: list[str], rows: list[list[str]]) :
        all_columns = ''
        for index in range(len(header_list)):
            column = self.__headline_cell(header_list[index], columns_weight_strech[index])

            first_row = True
            for row in rows:            
                column += self.__column_cell(row[index], columns_weight_strech[index], first_row)
                first_row = False

            all_columns += self.__single_column(column, columns_weight_strech[index])
        return self.__column_set(all_columns)
        
    def __column_set(self, all_columns : str):
        block = '''
        {{
         "type":"ColumnSet",
         "columns":[{0}]
        }},
        '''
        return block.format(all_columns)

    def __single_column(self, column_cells: str, width_strech : bool):
        block = '''
        {{
               "type":"Column",
               "width" : "{0}",
               "items":[{1}],
        }},
        '''
        return block.format(self.__width(width_strech),column_cells)

    def __headline_cell(self, text: str, width_strech : bool):
        block = '''
        {{
            "type":"TextBlock",
            "isSubtle":true,
            "text":"{0}",
            "weight":"bolder",
            "width111": "stretch",
        }},
        '''
        return block.format(text)
    
    def __column_cell(self, text: str, width_strech : bool, first_row : bool):
        separator = ''
        if (first_row):
            separator = '"separator": true'
        block = '''
        {{
            "type":"TextBlock",
            "isSubtle":true,
            "text":"{0}",
            "width111": "stretch",
            {1}
        }},
        '''
        return block.format(text, separator)

    def __width(self, width_strech : bool):
        if width_strech:
            return 'stretch'
        return 'auto'