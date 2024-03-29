import re
import sys
from typing import Callable, Any, Literal, Union
from alive_progress import alive_bar

import pandas as pd
from oneparams import config
from oneparams.config import CheckException
from oneparams.excel.checks import CheckTypes
from oneparams.utils import string_normalize


class Excel:

    def __init__(self,
                 book: pd.ExcelFile,
                 sheet_name: str,
                 header_row: int = 1,
                 verbose: bool = False):

        self.column_details: list = []
        self.verbose: bool = verbose
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
            excel.columns = excel.columns.astype("string")
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

        Caso tenha apenas 1 planilha no arquivo ela é retornada
        """
        if len(self.__book.sheet_names) == 1:
            return self.__book.sheet_names[0]

        for names in self.__book.sheet_names:
            name = string_normalize(names)
            if re.search(search, name, re.IGNORECASE):
                return names
        raise ValueError(
            f"ERROR! Sheet '{search}' not found! Rename your sheet!")

    def column_name(self, column_name: Union[str, list[str]]) -> str:
        """
        Resquias e retorna o nome da coluna da planilha,
        se não encontrar, retorna ValueError
        """
        excel = self.excel
        if isinstance(column_name, str):
            column_name = [column_name]

        for header in excel.keys():
            header_name = string_normalize(header)
            count = 0
            for name in column_name:
                if re.search(name, header_name, re.IGNORECASE):
                    count += 1
            if count == len(column_name):
                return header

        column_formated = " ".join(column_name)
        raise ValueError(f"Column '{column_formated}' not found!")

    def add_column(self,
                   key: str,
                   name: Union[str, list[str]],
                   required: bool = True,
                   default: Any = None,
                   types: Literal["string", "int", "float", "bool", "date",
                                  "time", "email", "cel", "cpf",
                                  "sex"] = "string",
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
                print(f"ERROR! Required {exp}")
                self.erros = True
            elif self.verbose and not config.NO_WARNING:
                print(f"WARNING! {exp}")
            excel[key] = default
        else:
            excel.rename({column_name: key}, axis='columns', inplace=True)

        self.column_details.append({
            "key": key,
            "types": types,
            "default": default,
            "length": length,
            "custom_function_before": custom_function_before,
            "custom_function_after": custom_function_after
        })

    def check_all(self,
                  check_row: Callable = None,
                  check_duplicated_keys: list[str] = None,
                  checks_final: list[Callable] = None) -> bool:
        """
        Função responsável por verificar todas as colunas
        da planilha

        Parâmetros:
        check_row: função que será executada para cada linha da planilha
        checks_final: lista de funções que serão executadas
            considerando todos os dados da planilha

        Retorno:
        False se NÃO ouve erros na verificação
        True se ouve erros na verificação
        """
        if self.erros:
            head = self.__header_row + 1
            print(f"ERROS FOUND! REMENBER HEADER ROW = {head}")
            sys.exit(1)

        excel = self.excel

        # configuração padrão da barra de progresso
        config.config_bar_excel()

        # verificando todas as colunas
        with alive_bar(len(excel.index) * len(self.column_details),
                       title="Checking for columns...") as pbar:
            # Verificações por coluna
            for column in self.column_details:
                for index in excel.index:
                    value = excel.at[index, column["key"]]
                    invalid = self.check_value(value=value,
                                               index=index,
                                               **column)
                    if invalid and not self.erros:
                        self.erros = True
                    pbar()

        # Verificações por linha
        with alive_bar(len(excel.index), title="Checking for rows...") as pbar:
            if check_row is not None:
                for row in excel.index:
                    try:
                        data = check_row(excel.at[row, "row"],
                                         excel.loc[row].copy())
                        for key, value in data.items():
                            excel.at[row, key] = value

                    except CheckException:
                        self.erros = True
                    pbar()

        # Verificações totais (duplicação de dados)
        if check_duplicated_keys is not None:
            try:
                excel = self.checks.check_duplications(
                    data=excel, keys=check_duplicated_keys)
            except CheckException:
                self.erros = True

        if checks_final is not None:
            for check in checks_final:
                try:
                    excel = check(excel)
                except CheckException:
                    self.erros = True
                pbar()

        self.excel = excel
        return self.erros

    def check_value(self,
                    value: Any,
                    key: str,
                    types: str,
                    index: int,
                    default: Any = None,
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

    def data_all(self) -> dict:
        excel = self.excel
        if excel.empty:
            return {}

        excel = excel.drop(columns="row")
        excel = excel.where(pd.notnull(excel), None)
        return excel.to_dict('records')
