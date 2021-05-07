import oneparams.config as config
from datetime import time

from oneparams.utils import get_bool, get_float, get_time
from oneparams.utils import get_cel, wprint, check_email


def check_types(self, data):
    excel = self.excel
    types = data["types"]
    length = data["length"]

    if types == "string":
        excel = excel.apply(lambda x: check_string(self, x, data, x.name),
                            axis=1)

    elif types == "time":
        excel = excel.apply(lambda x: check_time(self, x, data, x.name),
                            axis=1)

    elif types == "float":
        excel = excel.apply(lambda x: check_float(self, x, data, x.name),
                            axis=1)

    elif types == "bool":
        excel = excel.apply(lambda x: check_bool(self, x, data, x.name),
                            axis=1)

    elif types == "cel":
        excel = excel.apply(lambda x: check_cel(self, x, data, x.name), axis=1)

    elif types == "email":
        excel = excel.apply(lambda x: check_mail(self, x, data, x.name),
                            axis=1)

    if length not in (0, None):
        excel = excel.apply(
            lambda x: check_length(self, x, data, x.name, length), axis=1)

    return excel


def check_string(self, value, data, row):
    """
    Verificações de tipo string
    """
    # antes de fazer a verificação do tipo,
    # passa pela verificação padrão, se a função retornar
    # True, continua, Falso retorna os valores sem alteração
    if check_default(self, value, data):
        return value

    key = data["key"]
    value[key] = str(value[key]).strip()
    return value


def check_float(self, values, data, row):
    """
    Verificações de tipo float
    """
    # antes de fazer a verificação do tipo,
    # passa pela verificação padrão, se a função retornar
    # True, continua, Falso retorna os valores sem alteração
    if check_default(self, values, data):
        return values

    key = data["key"]
    value = values[key]

    try:
        value = get_float(value)
        values[key] = value
    except ValueError as exp:
        print("ERROR! in line {}: {}".format(self.row(row), exp))
        self.erros = True
    finally:
        return values


def check_time(self, values, data, row):
    # antes de fazer a verificação do tipo,
    # passa pela verificação padrão, se a função retornar
    # True, continua, Falso retorna os valores sem alteração
    if check_default(self, values, data):
        return values

    key = data["key"]
    value = values[key]
    try:
        index_value = get_time(value)
        value = str(time(*index_value[:3]))
    except TypeError as exp:
        print("ERROR! In line {}: {}".format(self.row(row), exp))
        self.erros = True
    else:
        values[key] = value

    return values


def check_bool(self, values, data, row):
    """
    Verifica se o valor pode ser convertido em booleano
    retorna os mesmo valores com as devidas alterações,
    se der algum problema coloca True em self.erros da class Excel
    """
    # antes de fazer a verificação do tipo,
    # passa pela verificação padrão, se a função retornar
    # True, continua, Falso retorna os valores sem alteração
    if check_default(self, values, data):
        return values

    key = data["key"]
    value = values[key]
    value = str(value).strip()
    value = get_bool(value)
    if value is None:
        print("ERROR! in line {}: not possible change value to bool".format(
            self.row(row)))
        self.erros = True
    values[key] = value
    return values


def check_cel(self, values, data, row):
    """
    Verificações de telefone,
    retira caracteres especiais deixando apenas números
    caso não for valido, retorna None no campo
    """
    # antes de fazer a verificação do tipo,
    # passa pela verificação padrão, se a função retornar
    # True, continua, Falso retorna os valores sem alteração
    if check_default(self, values, data):
        return values

    key = data["key"]
    value = values[key]
    try:
        value = get_cel(value)
    except ValueError as exp:
        if value is None:
            wprint(
                f'WARNING! in line {self.row(row)}, Column {key}: empty phone')
        elif not config.RESOLVE_ERROS:
            print(f'ERROR! in line {self.row(row)}: {exp}')
            self.erros = True
        else:
            wprint(
                f'WARNING! in line {self.row(row)}: Column {key} phone invalid'
            )
            value = data["default"]

    values[key] = value
    return values


def check_mail(self, values, data, row):
    key = data["key"]
    value = values[key]
    if not check_email(value):
        if not config.RESOLVE_ERROS:
            print(f'ERROR! in line {self.row(row)}: Email {value} not valid')
            self.erros = True
        else:
            wprint(
                f'WARNING! in line {self.row(row)}: Email {value} not valid')
            value = data["default"]

    values[key] = value
    return values


def check_length(self, values, data, row, length):
    """
    Verifica se o tamanho do texto é menor que a
    quantidade máxima permitida (length)
    """
    key = data["key"]
    if len(values[key]) > length and not config.RESOLVE_ERROS:
        print(
            f'ERROR! in line {self.row(row)}: Column {key} string {values[key]} size {len(values[key])}/{length}'
        )
        self.erros = True
    elif len(values[key]) > length:
        wprint(
            f'WARNING: in line {self.row(row)}: Column {key} string {values[key]} size {len(values[key])}/{length}'
        )
        values[key] = values[key].strip()[:length]

    return values


def check_default(self, value, data):
    """
    Verifica se o valor é igual ao valor padrão,
    se for retorna True, se não retorna False
    """
    key = data["key"]
    if value[key] is data["default"]:
        return True
    return False
