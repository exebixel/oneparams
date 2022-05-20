import sys
import re

import pandas as pd
from alive_progress import alive_bar
from oneparams import config
from oneparams.api.cidade import ApiCidade
from oneparams.api.client import ApiCliente
from oneparams.api.colaborador import ApiColaboradores
from oneparams.config import CheckException, config_bar_api, config_bar_excel
from oneparams.excel.excel import Excel
from oneparams.utils import print_error


def clientes(book: pd.ExcelFile, header: int = 0, reset: bool = False):
    ApiColaboradores()
    one = ApiCliente()

    print("analyzing spreadsheet")

    ex = Excel(book=book, sheet_name="client", header_row=header, verbose=True)

    ex.add_column(key="ativoCliente",
                  name="ativo",
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
    ex.add_column(key="sexo", name="sexo", types="sex", required=False)
    ex.add_column(key="aniversario",
                  name="aniversario",
                  types="date",
                  default=None,
                  required=False)
    ex.add_column(key="cep", name="cep", length=50, required=False)
    ex.add_column(key="endereco", name="endereco", length=50, required=False)
    ex.add_column(key="bairro", name="bairro", length=40, required=False)
    ex.add_column(key="complemento",
                  name="complemento",
                  length=50,
                  required=False)
    ex.add_column(key="numeroEndereco",
                  name="numero",
                  custom_function_after=check_numero_endereco,
                  required=False)
    ex.add_column(key="cidadeId", name="cidade", required=False)
    ex.add_column(key="estadoId", name="estado", required=False)

    ex.clean_columns()

    invalid = ex.check_all(
        check_row=checks,
        checks_final=[check_all, check_registered, skip_items])
    if invalid:
        sys.exit(1)

    print("creating clients")
    data = ex.data_all()

    len_data = len(data)
    if reset:
        len_data += len(one.items)

    config_bar_api()
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
        api = ApiCidade()
        city = api.submodule_id(city=data["cidadeId"], state=data["estadoId"])
        data["cidadeId"] = city["cidadesId"]
        data["estadoId"] = city["estadosId"]
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
        "cpf": "DUPLICATED! lines {} and {}: Client's CPF '{}'",
        "celular": "DUPLICATED! lines {} and {}: Client's phone '{}'",
    }

    duplicated = {}
    total = 0

    config_bar_excel()
    with alive_bar(len(clis), title="Calculating duplications...") as pbar:
        for col in clis:
            # Lista duplicidades todos os registros duplicados
            # sem manter nenhum
            duplicated[col] = data[data.duplicated(keep=False,
                                                   subset=col)][[col, "row"]]

            # Exclui items nulos
            duplicated[col] = duplicated[col].dropna(subset=[col])
            if not duplicated[col].empty:
                # altera o tipo dos dados (necessário para fazer o sort)
                duplicated[col] = duplicated[col].astype(str)
                # ordena a lista
                duplicated[col] = duplicated[col].sort_values(by=[col, "row"])
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
                        print(clis[col].format(duplicate.at[i, "row"],
                                               duplicate.at[n, "row"],
                                               duplicate.at[i, col]))

                    if i in data.index:
                        if col == "celular" and config.RESOLVE_ERROS:
                            data.loc[i, "celular"] = "00000000"
                        elif config.RESOLVE_ERROS:
                            data.drop(i, inplace=True)
                        else:
                            erros = True
                pbar()

    if not erros:
        return data

    raise CheckException


def check_registered(data: pd.DataFrame) -> pd.DataFrame:
    api_cols = ApiColaboradores()
    erros = False

    keys = ["email", "celular"]
    with alive_bar(len(api_cols.items) * len(keys),
                   title="Checking registered clients...") as pbar:
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
                pbar()

    if erros:
        raise CheckException

    return data


def skip_items(data: pd.DataFrame) -> pd.DataFrame:
    if not config.SKIP:
        return data

    one = ApiCliente()
    with alive_bar(len(one.items), receipt=True,
                   title="Skiping registered clients...") as pbar:
        for clis in one.items.values():
            # Exclui items já cadastrados no sistema do DataFrame
            data = data.drop(
                data[data.nomeCompleto == clis["nomeCompleto"]].index)
            pbar()

    return data
