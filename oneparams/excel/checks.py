from typing import Callable
import pandas as pd
import oneparams.config as config
from datetime import time, datetime

from oneparams.utils import get_bool, get_float, get_time, get_date
from oneparams.utils import print_error, print_warning
from oneparams.utils import get_cel, check_email


class CheckTypes():

    def get_type_function(self, type: str) -> Callable:
        return getattr(self, f'check_{type}')

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
                print_warning("in line {}, Column {}: number used will be {}".format(
                    row, key, default))
            return default

        try:
            values = get_float(values)
        except ValueError as exp:
            print("ERROR! In line {}, Column {}: {}".format(
                row, key, exp))
            raise Exception
        finally:
            return values

    def check_time(self, values: any, key: str, default: any, row: int):
        # antes de fazer a verificação do tipo,
        # passa pela verificação padrão, se a função retornar
        # True, continua, Falso retorna os valores sem alteração
        if self.check_default(values, default):
            if not pd.notnull(values):
                print_warning(
                    f"In line {row}, Column {key}: Time used will be {default}")
            return default

        value = values
        try:
            index_value = get_time(value)
            value = str(time(*index_value[:3]))
        except TypeError as exp:
            print("ERROR! In line {}, Column {}: {}".format(
                row, key, exp))
            raise Exception
        else:
            values = value

        return values

    def check_date(self, value: any, key: str, default: any, row: int):
        if self.check_default(value, default):
            return default

        try:
            date = get_date(value)
            value = datetime.strftime(date, "%Y-%m-%dT00:00:00")
        except ValueError as exp:
            print_error(f"in line {row}, Column {key}: {exp}")
            if not config.RESOLVE_ERROS:
                raise Exception
            else:
                value = default

        return value

    def check_bool(self, value: any, key: str, default: any, row: int):
        """
        Verifica se o valor pode ser convertido em booleano
        retorna os mesmo valores com as devidas alterações,
        se der algum problema coloca True em self.erros da class Excel
        """
        # antes de fazer a verificação do tipo,
        # passa pela verificação padrão, se a função retornar
        # True, continua, Falso retorna os valores sem alteração
        if self.check_default(value, default):
            return default

        value = str(value).strip()
        value = get_bool(value)
        if value is None:
            print(
                f"ERROR! in line {row}, Column {key}: not possible change value to bool")
            raise Exception
        return value

    def check_cel(self, value: any, key: str, default: any, row: int):
        """
        Verificações de telefone,
        retira caracteres especiais deixando apenas números
        caso não for valido, retorna None no campo
        """

        try:
            value = get_cel(value)
        except ValueError as exp:
            if not pd.notnull(value):
                print_warning(
                    f'in line {row}, Column {key}: empty phone')
            else:
                print_error(f"in line {row}, Column {key}: {exp}")
                if config.RESOLVE_ERROS:
                    raise Exception
                else:
                    value = default

        return value

    def check_email(self, value: any, key: str, default: any, row: int):
        if not check_email(value):
            print_error(f"in line {row}: Email {value} is not valid")
            if not config.RESOLVE_ERROS:
                raise Exception
            else:
                return default

        return value

    def check_length(self, value: any, key: str, row: int, length: int):
        """
        Verifica se o tamanho do texto é menor que a
        quantidade máxima permitida (length)
        """
        if value is None:
            return value

        if len(str(value)) > length:
            print_error(
                f"in line {row}, Column {key}: {value} size {len(str(value))}/{length}")
            if config.RESOLVE_ERROS:
                value = value.strip()[:length]
            else:
                raise Exception

        return value

    def check_default(self, value: int, default: any):
        """
        Verifica se o valor é igual ao valor padrão,
        se for retorna True, se não retorna False
        """
        if pd.isnull(value):
            return True
        if value == default:
            return True
        return False
