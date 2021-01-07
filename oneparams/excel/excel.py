import re
import sys
from datetime import time

import pandas as pd
import xlrd
from oneparams.utils import get_bool, get_float, get_time, string_normalize


class Excel:
    def __init__(self, book, sheet_name, header_row=1):
        self.column_details = []

        self.__keys = []
        self.__column_index = []
        self.__defaults = []
        self.__types = []

        self.__book = book

        try:
            excel = pd.read_excel(book,
                                  self.sheet_name(sheet_name),
                                  header=header_row)
            # retirando linhas e colunas em brando do Data Frame
            excel = excel.dropna(how="all")
            excel.dropna(how="all", axis=1, inplace=True)
            excel = excel.where(pd.notnull(excel), None)
            self.__excel = excel

        except ValueError as exp:
            sys.exit(exp)

        self.__header_row = header_row
        self.__previous = []

    def sheet_name(self, search):
        """
        Função responsável por pesquisa a string do parâmetro 'search'
        nas planilhas (sheets) do 'book' especificado no __init__
        e retornar o 1º nome de planilha que encontrar na pesquisa
        """
        for names in self.__book.sheet_names:
            name = string_normalize(names)
            if re.search(search, name, re.IGNORECASE):
                return names
        raise ValueError(f'Sheet {search} not found!')

    def column_name(self, column_name):
        """
        Resquias e retorna o nome da coluna da planilha,
        se não encontrar, retorna ValueError
        """
        excel = self.__excel
        for header in excel.keys():
            header_name = string_normalize(header)
            if re.search(column_name, header_name, re.IGNORECASE):
                return header
        raise ValueError(f'Column {column_name} not found!')

    def add_column(self,
                   key,
                   name,
                   required=True,
                   default=None,
                   types="string"):
        """
        Função responsável por adicionar as colunas que serão lidas
        da planilha \n
        Parâmetros: \n
        key: nome da chave do dicionario com os dados da coluna \n
        name: nome da coluna da planilha, não é necessário informar o
        nome completo da coluna, apenas uma palavra para busca, se o nome da
        coluna não foi encontrado o programa fechará \n
        default: se a coluna não for encontrada ou o valor não foi informado
        então será considerado o valor default \n
        types: tipo de dado que deve ser retirado da coluna \n
        required: define se a coluna é obrigatória na planilha
        """
        excel = self.__excel
        try:
            column_name = self.column_name(name)
        except ValueError as exp:
            if required:
                sys.exit(exp)
            excel[key] = default
        else:
            excel.rename({column_name: key}, axis='columns', inplace=True)
            if default is not None:
                excel[key].fillna(value=default, inplace=True)

        self.column_details.append({
            "key": key,
            "type": types,
        })

    def row(self, index):
        """
        Retorna a linha do respectivo index passado
        """
        return index + self.__header_row + 2

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
                        erros = True

            elif types[i] == "string":
                index_value = str(index_value).strip()

            elif types[i] == "float":
                try:
                    index_value = get_float(index_value)
                except ValueError as exp:
                    print("ERROR! in line {}: {}".format(row + 1, exp))
                    erros = True

            elif types[i] == "bool":
                index_value = str(index_value).strip()
                index_value = get_bool(index_value)
                if index_value is None:
                    print(
                        "ERROR! in line {}: not possible change value to bool".
                        format(row + 1))
                    erros = True

            data[keys[i]] = index_value

        if check_row is not None:
            try:
                data = check_row(row, data, self.__previous)
            except Exception:
                erros = True

        if type(data) is dict:
            prev = {"row": row, "data": data}
            self.__previous.append(prev)
        elif type(data) is list:
            for i in data:
                prev = {"row": row, "data": i}
                self.__previous.append(prev)

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
