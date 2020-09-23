import re
import sys
from datetime import time

import xlrd

from oneparams.utils import get_bool, get_float, get_time, string_normalize


class Excel:
    def __init__(self, book, sheet_name, header_row=1):
        self.__keys = []
        self.__column_index = []
        self.__defaults = []
        self.__types = []

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

    def add_column(self,
                   key,
                   name,
                   required=True,
                   default=None,
                   types="string"):
        column_index = self.column_index(name)
        if column_index == -1 and required:
            print("column {} not found!!".format(name))
            sys.exit()

        self.__column_index.append(column_index)
        self.__keys.append(key)
        self.__defaults.append(default)
        self.__types.append(types)

    def data_row(self, row, check_row=None):
        keys = self.__keys
        index = self.__column_index
        default = self.__defaults
        types = self.__types
        sh = self.__sh

        data = {}
        erros = False
        for i in range(len(self.__keys)):
            if index[i] == -1:
                index_value = default[i]
                data[keys[i]] = index_value
                continue

            index_type = sh.cell_type(row, index[i])
            index_value = sh.cell_value(row, index[i])

            if index_type == xlrd.XL_CELL_EMPTY:
                index_value = default[i]

            elif types[i] == "time":
                if index_type == xlrd.XL_CELL_DATE:
                    index_value = xlrd.xldate_as_tuple(index_value,
                                                       self.__book.datemode)
                    index_value = str(time(*index_value[3:]))
                if index_type == xlrd.XL_CELL_TEXT:
                    index_value = str(index_value).strip()
                    try:
                        index_value = get_time(index_value)
                        index_value = str(time(*index_value[:3]))
                    except TypeError as exp:
                        print("ERROR! In line {}: {}".format(row + 1, exp))

            elif types[i] == "string":
                index_value = str(index_value).strip()

            elif types[i] == "float":
                try:
                    index_value = get_float(index_value)
                except ValueError as exp:
                    print("ERROR! in line {}: {}".format(row + 1, exp))

            elif types[i] == "bool":
                index_value = str(index_value).strip()
                index_value = get_bool(index_value)
                if index_value is None:
                    print(
                        "ERROR! in line {}: not possible change value to bool".
                        format(row + 1))

            data[keys[i]] = index_value

        if check_row is not None:
            try:
                data = check_row(row, data)
            except Exception:
                erros = True

        if erros:
            raise Exception
        return data

    def data_all(self, check_row=None):
        data = []
        erros = False
        for row in range(self.__header_row + 1, self.nrows):
            try:
                data_row = self.data_row(row, check_row=check_row)
            except Exception:
                erros = True
            if not erros:
                if type(data_row) is dict:
                    data.append(data_row)
                elif type(data_row) is list:
                    for i in data_row:
                        data.append(i)

        if erros:
            sys.exit()
        return data
