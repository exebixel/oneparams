import re
import sys
from datetime import time

import xlrd
from oneparams.utils import string_normalize


class Excel:
    def __init__(self, book, sheet_name, header_row=1):
        self.__keys = []
        self.__column_index = []
        self.__defaults = []

        self.__book = book
        sh_index = self.sheet_index(book, sheet_name)
        if sh_index == -1:
            print("sheet {0} not found!".format(sheet_name))
            sys.exit()
        self.__sh = book.sheet_by_index(sh_index)
        self.__header_row = header_row
        self.nrows = self.__sh.nrows

    def sheet_index(self, book, sheet_name):
        cont = 0
        for names in book.sheet_names():
            names = string_normalize(names)
            if (re.search(sheet_name, names, re.IGNORECASE)):
                break
            cont += 1
        else:
            return -1
        return cont

    def column_index(self, column_name):
        cont = 0
        for header in range(self.__sh.ncols):
            header_name = self.__sh.cell_value(rowx=1, colx=header)
            header_name = string_normalize(header_name)

            if (re.search(column_name, header_name, re.IGNORECASE)):
                break
            cont += 1
        else:
            return -1
        return cont

    def add_column(self, key, name, required=True, default=None):
        column_index = self.column_index(name)
        if column_index == -1 and required:
            print("column {} not found!!".format(name))
            sys.exit()

        self.__column_index.append(column_index)
        self.__keys.append(key)
        self.__defaults.append(default)

    def data_row(self, row):
        keys = self.__keys
        index = self.__column_index
        default = self.__defaults
        sh = self.__sh

        data = {}
        for i in range(len(self.__keys)):
            if index[i] == -1:
                index_value = default[i]
                data[keys[i]] = index_value
                continue

            index_type = sh.cell_type(row, index[i])
            index_value = sh.cell_value(row, index[i])

            if index_type == xlrd.XL_CELL_EMPTY:
                index_value = default[i]

            elif index_type == xlrd.XL_CELL_DATE:
                index_value = xlrd.xldate_as_tuple(index_value,
                                                   self.__book.datemode)
                index_value = str(time(*index_value[3:]))

            elif index_type == xlrd.XL_CELL_TEXT:
                index_value = index_value.strip()

            data[keys[i]] = index_value
        return data

    def data_all(self):
        data = []
        for row in range(self.__header_row + 1, self.nrows):
            data.append(self.data_row(row))
        return data
