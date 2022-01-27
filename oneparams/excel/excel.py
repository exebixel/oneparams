import re
import sys
from typing import Callable

import pandas as pd
from oneparams.config import CheckException
from oneparams.excel.checks import CheckTypes
from oneparams.utils import string_normalize


class Excel:

    def __init__(self,
                 book: pd.ExcelFile,
                 sheet_name: str,
                 header_row: int = 1):

        self.column_details = []
        self.__book = book

        self.erros: bool = False
        """
        indica se ouve algum erro nas validações da planilha
        se tiver erro o método data_all não deve
        retornar dados
        """

        self.excel: pd.DataFrame
        try:
            excel = pd.read_excel(book,
                                  self.sheet_name(sheet_name),
                                  header=header_row)
            # retirando linhas e colunas em brando do Data Frame
            excel = excel.dropna(how="all")
            excel.columns.astype("string")
            excel = excel.loc[:, ~excel.columns.str.contains('^Unnamed')]
            excel = excel.astype(object)
            excel = excel.where(pd.notnull(excel), None)
            self.excel = excel

        except ValueError as exp:
            sys.exit(exp)

        self.__header_row = header_row
        self.add_row_column()

        self.checks = CheckTypes()

    def sheet_name(self, search: str) -> str:
        """
        Função responsável por pesquisa a string do parâmetro 'search'
        nas planilhas (sheets) do 'book' especificado no __init__
        e retornar o 1º nome de planilha que encontrar na pesquisa
        """
        for names in self.__book.sheet_names:
            name = string_normalize(names)
            if re.search(search, name, re.IGNORECASE):
                return names
        raise ValueError(f'ERROR! Sheet {search} not found!')

    def column_name(self, column_name: str) -> str:
        """
        Resquias e retorna o nome da coluna da planilha,
        se não encontrar, retorna ValueError
        """
        excel = self.excel
        for header in excel.keys():
            header_name = string_normalize(header)
            if re.search(column_name, header_name, re.IGNORECASE):
                return header

        head = self.__header_row + 1
        raise ValueError(
            f'ERROR! Column {column_name} not found! Header is line {head}')

    def add_column(self,
                   key: str,
                   name: str,
                   required: bool = True,
                   default: any = None,
                   types: str = "string",
                   length: int = 0,
                   custom_function_before: Callable = None,
                   custom_function_after: Callable = None):
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
        padrão 1 ou seja ilimitado \n

        custom_function: recebe a referencia de uma função que sera executada
            apos as verificações padrão, essa função deve conter os parametros:
            value: (valor que sera verificado),
            key: (Chave do valor que sera verificado, para fins de log),
            row: (Linha da planilha que esta o valor que sera verificado,
                para fins de log),
            default: (Valor padrão que deve ser usado caso caso ocorra algum
                erro na verificação, para resolução de problemas).
            Essa custom_funcition deverá retornar o valor (value) verificado
            em caso de sucesso na verficação/tratamento, caso contratio,
            deve retornar uma Exception
        """
        excel = self.excel

        try:
            column_name = self.column_name(name)
        except ValueError as exp:
            if required:
                sys.exit(exp)
            excel[key] = default
        else:
            excel.rename({column_name: key}, axis='columns', inplace=True)

        self.check_column(key=key,
                          types=types,
                          default=default,
                          length=length,
                          custom_function_before=custom_function_before,
                          custom_function_after=custom_function_after)

        self.column_details.append({
            "key": key,
            "type": types,
            "default": default
        })

    def check_column(self,
                     key: str,
                     types: str,
                     default: any,
                     length: int = 0,
                     custom_function_before: Callable = None,
                     custom_function_after: Callable = None):

        for index, data in self.excel.iterrows():
            erros = self.check_value(
                value=data[key],
                key=key,
                types=types,
                default=default,
                index=index,
                length=length,
                custom_function_before=custom_function_before,
                custom_function_after=custom_function_after)

            if erros and not self.erros:
                self.erros = erros

    def check_value(self,
                    value: any,
                    key: str,
                    types: str,
                    index: int,
                    default: any = None,
                    length: int = 0,
                    custom_function_before: Callable = None,
                    custom_function_after: Callable = None) -> bool:
        """ Executa todas as verificações em um valor especifico,
        retorna True um False para caso as verificações passarem ou não
        """
        excel = self.excel
        erros = False

        # Pega referencia fa função de verificação padrão
        check_function = self.checks.get_type_function(types=types)

        # Verificações customizadas que serão feitas antes
        # das verificações padrões
        if custom_function_before is not None:
            try:
                value = custom_function_before(value=value,
                                               key=key,
                                               default=default,
                                               row=self.row(index))
            except CheckException:
                erros = True

        # Executa a verificação padrão
        try:
            value = check_function(value,
                                   key=key,
                                   default=default,
                                   row=self.row(index))
        except CheckException:
            erros = True

        # Verificação de tamanho de string
        if length not in (0, None):
            try:
                value = self.checks.check_length(value,
                                                 key=key,
                                                 row=self.row(index),
                                                 length=length)
            except CheckException:
                erros = True

        # Executa a função de verificações customizada
        # depois das verificações padrão
        if custom_function_after is not None:
            try:
                value = custom_function_after(value=value,
                                              key=key,
                                              default=default,
                                              row=self.row(index))
            except CheckException:
                erros = True

        excel.at[index, key] = value
        return erros

    def clean_columns(self):
        """
        Deleta as colunas do data frame que não foram adicionadas pelo
        'add_column'
        """
        columns = list(map(lambda col: col["key"], self.column_details))
        columns.append("row")
        self.excel = self.excel[columns]

    def row(self, index: int) -> int:
        """
        Retorna a linha do respectivo index passado
        """
        return index + self.__header_row + 2

    def add_row_column(self):
        """ Adicionar uma columa ao datafreme chamada 'row'
        com o número de cada linha
        """
        excel = self.excel
        rows = []
        for i in excel.index:
            rows.append(self.row(i))
        excel["row"] = rows

    def data_row(self, row: int, check_row: Callable = None) -> None:
        excel = self.excel

        if check_row is not None:
            try:
                excel.loc[row] = check_row(self.row(row),
                                           excel.loc[row].copy())
            except CheckException:
                self.erros = True

        if self.erros:
            raise CheckException

    def data_all(self,
                 check_row: Callable = None,
                 checks_final: list[Callable] = None) -> dict:
        excel = self.excel
        for row in excel.index:
            try:
                self.data_row(row, check_row=check_row)
            except CheckException:
                self.erros = True

        if checks_final is not None:
            for check in checks_final:
                try:
                    excel = check(excel)
                except CheckException:
                    self.erros = True

        if self.erros:
            sys.exit(1)

        excel = excel.drop(columns="row")
        excel = excel.where(pd.notnull(excel), None)
        return excel.to_dict('records')
