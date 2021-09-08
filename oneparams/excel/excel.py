import re
import sys

import pandas as pd

from oneparams.utils import string_normalize
from oneparams.excel.checks import check_types


class Excel:
    def __init__(self, book, sheet_name, header_row=1):
        self.column_details = []

        self.__keys = []
        self.__column_index = []
        self.__defaults = []
        self.__types = []

        self.__book = book

        self.erros = False
        """
        indica se ouve algum erro nas validações da planilha
        se tiver erro o método data_all não deve
        retornar dados
        """

        try:
            excel = pd.read_excel(book,
                                  self.sheet_name(sheet_name),
                                  header=header_row)
            # retirando linhas e colunas em brando do Data Frame
            excel = excel.dropna(how="all")
            # excel.dropna(how="all", axis=1, inplace=True)
            excel = excel.loc[:, ~excel.columns.str.contains('^Unnamed')]
            excel = excel.where(pd.notnull(excel), None)
            self.excel = excel

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
        excel = self.excel
        for header in excel.keys():
            header_name = string_normalize(header)
            if re.search(column_name, header_name, re.IGNORECASE):
                return header
        raise ValueError(f'ERROR! Column {column_name} not found! Remember the Header is line {self.__header_row + 1}')

    def add_column(self,
                   key,
                   name,
                   required=True,
                   default=None,
                   types="string",
                   length=0):
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
        required: define se a coluna é obrigatória na planilha \n
        length: Número máximo de caracteres que o dado pode ter,
        padrão 0 ou seja ilimitado
        """
        excel = self.excel

        data = {
            "key": key,
            "name": name,
            "required": required,
            "default": default,
            "types": types,
            "length": length
        }

        try:
            column_name = self.column_name(name)
        except ValueError as exp:
            if required:
                sys.exit(exp)
            excel[key] = default
        else:
            excel.rename({column_name: key}, axis='columns', inplace=True)
            # if default is not None:
            #     excel[key].fillna(value=default, inplace=True)

        self.excel = check_types(self, data)

        self.column_details.append({
            "key": key,
            "type": types,
            "default": default
        })

    def clean_columns(self):
        """
        Deleta as colunas do data frame que não foram adicionadas pelo
        'add_column'
        """
        self.excel.drop(self.excel.columns.difference(
            map(lambda col: col["key"], self.column_details)),
                        axis=1,
                        inplace=True)

    def row(self, index):
        """
        Retorna a linha do respectivo index passado
        """
        return index + self.__header_row + 2

    def add_row_column(self):
        excel = self.excel
        rows = []
        for i in excel.index:
            rows.append(self.row(i))
        excel["row"] = rows

    def data_row(self, row, check_row=None):
        excel = self.excel

        if check_row is not None:
            try:
                excel.loc[row] = check_row(self.row(row),
                                           excel.loc[row].copy())
            except Exception:
                self.erros = True

        if self.erros:
            raise Exception

    def data_all(self, check_row=None, check_final=None):
        excel = self.excel
        for row in excel.index:
            try:
                self.data_row(row, check_row=check_row)
            except Exception:
                self.erros = True

        if check_final is not None:
            try:
                excel = check_final(self, excel)
            except Exception:
                self.erros = True

        if self.erros:
            sys.exit()
        return excel.to_dict('records')
