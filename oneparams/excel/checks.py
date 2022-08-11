""" Modulo com as verificações e tratamentos de padrões
"""
import re
from datetime import datetime, time
from typing import Any, Callable

from pandas import DataFrame, notnull, isnull
from alive_progress import alive_bar
from oneparams import config
from oneparams.config import CheckException, config_bar_excel
from oneparams.utils import (check_email, get_bool, get_cel, get_cpf, get_date,
                             get_float, get_int, get_sex, get_time,
                             print_error, print_warning)


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

    def check_string(self, value: Any, key: str, default: Any,
                     row: int) -> Any:
        """
        Verificações de tipo string
        """
        if self.check_default(value, default):
            return default

        return str(value).strip()

    def check_float(self, value: Any, key: str, default: Any, row: int) -> Any:
        """
        Verificações de tipo float
        """
        if self.check_default(value, default):
            if not notnull(value):
                print_warning(
                    f"In line {row}, Column {key}: value will be {default}")
            return default

        try:
            value = get_float(value)
        except ValueError as exp:
            print_error(f"In line {row}, Column {key}: {exp}")
            if not config.RESOLVE_ERROS:
                raise config.CheckException from exp
            value = default

        return value

    def check_int(self, value: Any, key: str, default: Any, row: int) -> Any:
        """
        Verificações padrão do tipo INT
        """
        if self.check_default(value, default):
            return default

        try:
            value = get_int(value)
        except ValueError as exp:
            print_error(f"in line {row}, Column {key}: {exp}")
            if not config.RESOLVE_ERROS:
                raise config.CheckException from exp
            value = default

        return value

    def check_time(self, value: Any, key: str, default: Any, row: int) -> Any:
        """ Verificações padrão do tipo TIME """
        if self.check_default(value, default):
            if not notnull(value):
                print_warning(
                    f"In line {row}, Column {key}: value will be {default}")
            return default

        try:
            index_value = get_time(value)
            value = str(time(*index_value[:3]))
        except TypeError as exp:
            print(f"ERROR! In line {row}, Column {key}: {exp}")
            raise config.CheckException

        return value

    def check_date(self, value: Any, key: str, default: Any, row: int) -> Any:
        """ Verificações padrão do tipo DATE
        """
        if self.check_default(value, default):
            return default

        try:
            date = get_date(value)
            value = datetime.strftime(date, "%Y-%m-%dT00:00:00")
        except ValueError as exp:
            print_error(f"in line {row}, Column {key}: '{value}' is not valid")
            if not config.RESOLVE_ERROS:
                raise config.CheckException from exp
            value = default

        return value

    def check_bool(self, value: Any, key: str, default: Any, row: int) -> Any:
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

    def check_cel(self, value: Any, key: str, default: Any, row: int) -> Any:
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
            if not config.RESOLVE_ERROS:
                raise config.CheckException
            value = default

        return value

    def check_email(self, value: Any, key: str, default: Any, row: int) -> Any:
        """ Verificações padrão do tipo EMAIL
        """
        if self.check_default(value, default):
            print_warning(f"in line {row}, Column {key}: empty email")
            return default

        email = check_email(value)
        if email is None:
            print_error(f"in line {row}, Column {key}: '{value}' is not valid")
            if not config.RESOLVE_ERROS:
                raise config.CheckException
            return default

        return email

    def check_cpf(self, value: Any, key: str, default: Any, row: int) -> Any:
        if self.check_default(value, default):
            return default

        value = re.sub(r'\.0$', '', str(value))
        cpf = get_cpf(value)
        if cpf is None:
            print_error(
                f"in line {row}, Column {key}: '{value}' is invalid CPF")
            if not config.RESOLVE_ERROS:
                raise config.CheckException
            return default
        return cpf

    def check_sex(self, value: Any, key: str, default: Any, row: int) -> Any:
        if self.check_default(value, default):
            return default

        sex = get_sex(value)
        if sex is None:
            print_error(f"In line {row}, Column {key}: '{value}' is not valid")
            if config.RESOLVE_ERROS:
                return default

        return sex

    def check_length(self, value: Any, key: str, row: int, length: int) -> Any:
        """
        Verifica se o tamanho do texto é menor que a
        quantidade máxima permitida (length)
        """
        if self.check_default(value, None):
            return value

        size = len(str(value))
        if size > length:
            print_error(
                f"in line {row}, Column {key}: '{value}' size {size}/{length}")
            if config.RESOLVE_ERROS:
                value = value.strip()[:length]
            else:
                raise config.CheckException

        return value

    def check_default(self, value: Any, default: Any) -> bool:
        """
        Verifica se o valor é igual ao valor padrão,
        se for retorna True, se não retorna False
        """
        if isnull(value):
            return True
        if value == default:
            return True
        return False

    def check_duplications(self, data: DataFrame,
                           keys: list[str]) -> DataFrame:
        """
        Verifica se há duplicatas no dataframe
        """
        erros = False

        duplicated = {}
        total = 0

        config_bar_excel()
        with alive_bar(len(keys), title="Calculating duplications...") as pbar:
            for col in keys:
                # Lista duplicidades todos os registros duplicados
                # sem manter nenhum
                duplicated[col] = data[data.duplicated(
                    keep=False, subset=col)][[col, "row"]]

                # Exclui items nulos
                duplicated[col] = duplicated[col].dropna(subset=[col])
                if not duplicated[col].empty:
                    # altera o tipo dos dados (necessário para fazer o sort)
                    duplicated[col][col] = duplicated[col][col].astype(str)
                    # ordena a lista
                    duplicated[col] = duplicated[col].sort_values(
                        by=[col, "row"])
                    total += len(duplicated[col].index)
                else:
                    duplicated.pop(col)
                pbar()

        with alive_bar(total, title="Resolving duplications...") as pbar:
            # Verfica duplicidades no DataFrame
            for col, duplicate in duplicated.items():
                index = iter(duplicate.index)
                next(index)
                for i in duplicate.index:
                    n = next(index, None)
                    if (n is not None
                            and duplicate.at[i, col] == duplicate.at[n, col]):
                        if not config.RESOLVE_ERROS or not config.NO_WARNING:
                            line1 = duplicate.at[i, "row"]
                            line2 = duplicate.at[n, "row"]
                            value = duplicate.at[i, col]
                            p = "DUPLICATED! lines {} and {}, Column {}: value '{}'"
                            print(p.format(line1, line2, col, value))

                        if i in data.index and config.RESOLVE_ERROS:
                            data.drop(i, inplace=True)
                        else:
                            erros = True
                    pbar()

        if not erros:
            return data

        raise CheckException
