""" Modulo com as verificações e tratamentos de padrões
"""
from datetime import datetime, time
from typing import Callable

import pandas as pd
from oneparams import config
from oneparams.utils import (check_email, get_bool, get_cel, get_date,
                             get_float, get_time, print_error, print_warning)


class CheckTypes():
    """ Nessa Classe contem os netodos de verificações padrão \n

    Todos os metodos de verificação devem possuir como parametros \n
    value: valor a ser verificado, \n
    key: chave do valor que sera verificado (usado para log), \n
    row: linha da planilha em que o dado (value) esta (usado para log), \n
    default: valor padrão a ser usado caso as verificações não passem
    (usado apenas com RESOLVE_ERROS = True)

    E irão retornar o value ao final das verificações e tratamentos,
    caso alguma verificação não passe devera retornar uma Exception
    """

    def get_type_function(self, types: str) -> Callable:
        """ Retorna a função referente ao tipo de verificação
        """
        return getattr(self, f'check_{types}')

    def check_string(self, values: any, key: str, default: any, row: int):
        """
        Verificações de tipo string
        """
        if self.check_default(values, default):
            return default

        return str(values).strip()

    def check_float(self, values: any, key: str, default: any, row: int):
        """
        Verificações de tipo float
        """
        if self.check_default(values, default):
            if not pd.notnull(values):
                print_warning(
                    f"In line {row}, Column {key}: value will be {default}")
            return default

        try:
            values = get_float(values)
        except ValueError as exp:
            print_error(f"In line {row}, Column {key}: {exp}")
            raise config.CheckException
        return values

    def check_time(self, values: any, key: str, default: any, row: int):
        """ Verificações padrão do tipo TIME """
        if self.check_default(values, default):
            if not pd.notnull(values):
                print_warning(
                    f"In line {row}, Column {key}: value will be {default}")
            return default

        value = values
        try:
            index_value = get_time(value)
            value = str(time(*index_value[:3]))
        except TypeError as exp:
            print(f"ERROR! In line {row}, Column {key}: {exp}")
            raise config.CheckException
        else:
            values = value

        return values

    def check_date(self, value: any, key: str, default: any, row: int):
        """ Verificações padrão do tipo DATE
        """
        if self.check_default(value, default):
            return default

        try:
            date = get_date(value)
            value = datetime.strftime(date, "%Y-%m-%dT00:00:00")
        except ValueError as exp:
            print_error(f"in line {row}, Column {key}: {exp}")
            if not config.RESOLVE_ERROS:
                raise config.CheckException
            value = default

        return value

    def check_bool(self, value: any, key: str, default: any, row: int):
        """
        Verifica se o valor pode ser convertido em booleano
        retorna os mesmo valores com as devidas alterações
        """

        if self.check_default(value, default):
            return default

        value = str(value).strip()
        value = get_bool(value)
        if value is None:
            print(
                f"ERROR! in line {row}, Column {key}: can't get boolean value")
            raise config.CheckException
        return value

    def check_cel(self, value: any, key: str, default: any, row: int):
        """
        Verificações de telefone,
        retira caracteres especiais deixando apenas números
        caso não for valido, retorna None no campo
        """
        if self.check_default(value, default):
            print_warning(f"in line {row}, Column {key}: empty phone")
            return default

        try:
            value = get_cel(value)
        except ValueError as exp:
            print_error(f"in line {row}, Column {key}: {exp}")
            if config.RESOLVE_ERROS:
                raise config.CheckException
            value = default

        return value

    def check_email(self, value: any, key: str, default: any, row: int):
        """ Verificações padrão do tipo EMAIL
        """
        if self.check_default(value, default):
            print_warning(f"in line {row}, Column {key}: empty email")
            return default

        if not check_email(value):
            print_error(f"in line {row}, Column {key}: {value} is not valid")
            if not config.RESOLVE_ERROS:
                raise config.CheckException
            return default

        return value

    def check_length(self, value: any, key: str, row: int, length: int):
        """
        Verifica se o tamanho do texto é menor que a
        quantidade máxima permitida (length)
        """
        if self.check_default(value, None):
            return value

        size = len(str(value))
        if size > length:
            print_error(
                f"in line {row}, Column {key}: {value} size {size}/{length}")
            if config.RESOLVE_ERROS:
                value = value.strip()[:length]
            else:
                raise config.CheckException

        return value

    def check_default(self, value: any, default: any):
        """
        Verifica se o valor é igual ao valor padrão,
        se for retorna True, se não retorna False
        """
        if pd.isnull(value):
            return True
        if value == default:
            return True
        return False
