import xlrd, sys, re
from utils import *

class excel:

    def __init__(self, book, sheet_name):
        self.__keys = []
        self.__column_index = []

        sh_index = self.sheet_index(book, sheet_name)
        if sh_index == -1:
            print("sheet {0} not found!".format(sheet_name))
            sys.exit()
        self.__sh = book.sheet_by_index(sh_index)
        self.nrows = self.__sh.nrows

    def sheet_index(self, book, sheet_name):
        cont = 0
        for names in book.sheet_names():
            names = string_normalize(names)
            if ( re.search(sheet_name, names, re.IGNORECASE) ):
                break
            cont+=1
        else:
            return -1
        return cont

    def column_index(self, column_name):
        cont = 0
        for header in range(self.__sh.ncols):
            header_name = self.__sh.cell_value(rowx=1, colx=header)
            header_name = string_normalize(header_name)

            if ( re.search(column_name, header_name, re.IGNORECASE) ):
                break
            cont+=1
        else:
            return -1
        return cont

    def add_column(self, key, name):
        column_index = self.column_index(name)
        if column_index == -1:
            print("column not found!!")
            sys.exit()

        self.__column_index.append(column_index)
        self.__keys.append(key)


    def data_row(self, row):
        keys = self.__keys
        index = self.__column_index
        data = {}
        for i in range( len(self.__keys) ):
            index_value = self.__sh.cell_value(rowx=row, colx=index[i])
            index_value = str(index_value).strip()
            data[ keys[i] ] = index_value

        return data
