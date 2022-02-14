import re

import pandas as pd
from alive_progress import alive_bar
from oneparams import config
from oneparams.api.client import ApiCliente
from oneparams.api.colaborador import ApiColaboradores
from oneparams.config import CheckException, config_bar
from oneparams.excel.excel import Excel
from oneparams.utils import print_error, wprint


def clientes(book: pd.ExcelFile, header: int = 0, reset: bool = False):
    ApiColaboradores()
    one = ApiCliente()

    print("analyzing spreadsheet")

    ex = Excel(book=book, sheet_name="client", header_row=header)

    ex.add_column(key="ativoCliente",
                  name="ativoCliente",
                  default=True,
                  types="bool",
                  required=False)
    ex.add_column(key="nomeCompleto",
                  name="nome",
                  length=50,
                  custom_function_after=check_nome_completo)
    ex.add_column(key="email", name="email", types="email", length=50)
    ex.add_column(key="celular", name="celular", types="cel")
    ex.add_column(key="cpf", name="cpf", types="cpf")
    ex.add_column(key="sexo", name="sexo", types="sex")
    ex.add_column(key="aniversario",
                  name="aniversario",
                  types="date",
                  default=None,
                  required=False)
    ex.add_column(key="cep", name="cep", length=50)
    ex.add_column(key="endereco", name="endereco", length=50)
    ex.add_column(key="bairro", name="bairro", length=40)
    ex.add_column(key="complemento", name="complemento", length=50)
    ex.add_column(key="numeroEndereco",
                  name="numero",
                  custom_function_after=check_numero_endereco)
    ex.add_column(key="cidadeId", name="cidade")
    ex.add_column(key="estadoId", name="estado")

    ex.clean_columns()
    ex.add_row_column()

    data = ex.data_all(check_row=checks,
                       checks_final=[check_all, check_registered, skip_items])

    len_data = len(data)
    if reset:
        len_data += len(one.items)

    config_bar()
    with alive_bar(len_data) as pbar:
        if reset:
            for i in list(one.items):
                one.delete(i)
                pbar()

        for row in data:
            one.diff_item(row)
            pbar()


def checks(row: int, data: dict) -> dict:
    try:
        api = ApiCliente()
        data = api.name_to_id(data)
    except ValueError as exp:
        print_error(f"in line {row}: {exp}")
        data["cidadeId"] = None
        data["estadoId"] = None
        if not config.RESOLVE_ERROS:
            raise CheckException from exp

    return data


def check_nome_completo(value: any, key: str, row: int, default: any) -> any:
    if pd.isnull(value):
        print(f"ERROR! in line {row}, Column {key}: Empty name")
        raise CheckException
    return value


def check_numero_endereco(value: any, key: str, row: int, default: any) -> any:
    if pd.isnull(value):
        return default

    value = re.sub(r'\.0$', '', str(value))
    if not value.isdecimal():
        print_error(f"in line {row}, column {key}: is not a number")
        if not config.RESOLVE_ERROS:
            raise CheckException
        return default

    if len(value) > 4:
        print_error(
            f"in line {row}, Column {key}: {value} size {len(value)}/4")
        if not config.RESOLVE_ERROS:
            raise CheckException
        return default

    return value


def check_all(data: pd.DataFrame) -> pd.DataFrame:
    erros = False
    clis = {
        "nomeCompleto": "DUPLICATED! in lines {} and {}: Client '{}'",
        "email": "DUPLICATED! lines {} and {}: Client's email '{}'",
        "celular": "DUPLICATED! lines {} and {}: Client's phone '{}'",
        "cpf": "DUPLICATED! lines {} and {}: Client's CPF '{}'"
    }

    for col, print_erro in clis.items():
        duplic = data[data.duplicated(keep=False, subset=col)]

        # Verfica duplicidades no DataFrame
        for i in duplic.loc[data[col].notnull()].index:
            for j in duplic.loc[data[col].notnull()].index:
                if (duplic.loc[i, col] == duplic.loc[j, col] and j != i):
                    message = print_erro.format(duplic.loc[i, "row"],
                                                duplic.loc[j, "row"],
                                                duplic.loc[i, col])
                    duplic = duplic.drop(index=i)

                    if col == "celular":
                        data.loc[i, col] = "00000000"
                    else:
                        data = data.drop(index=i)

                    if config.RESOLVE_ERROS:
                        wprint(message)
                    else:
                        print(message)
                        erros = True

                    break

    if erros:
        raise CheckException

    return data


def check_registered(data: pd.DataFrame) -> pd.DataFrame:
    api_cols = ApiColaboradores()
    erros = False

    keys = ["email", "celular"]
    for key in keys:
        for cols in api_cols.items.values():
            registered_emails = data[data[key] == cols[key]]
            if not registered_emails.empty:
                row = registered_emails['row'].values[0]
                value = cols[key]
                print_error(
                    f"in line {row}, Column {key}: '{value}' already registered as collaborator"
                )
                data = data.drop(registered_emails.index)
                if not config.RESOLVE_ERROS:
                    erros = True

    if erros:
        raise CheckException

    return data


def skip_items(data: pd.DataFrame) -> pd.DataFrame:
    if not config.SKIP:
        return data

    one = ApiCliente()
    print("skipping clients already registered")
    for clis in one.items.values():
        # Exclui items já cadastrados no sistema do DataFrame
        data = data.drop(data[data.nomeCompleto == clis["nomeCompleto"]].index)

    return data
