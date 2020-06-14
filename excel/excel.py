import xlrd, sys, re
from utils import *

def sheet_index(book, sheet_name):
    cont = 0
    for names in book.sheet_names():
        names = string_normalize(names)
        if ( re.search(sheet_name, names, re.IGNORECASE) ):
            break
        cont+=1
    else:
        return -1
    return cont

def column_index(sheet, column_name):
    cont = 0
    for header in range(sheet.ncols):
        header_name = sheet.cell_value(rowx=1, colx=header)
        header_name = string_normalize(header_name)

        if ( re.search(column_name, header_name, re.IGNORECASE) ):
            break
        cont+=1
    else:
        return -1
    return cont
