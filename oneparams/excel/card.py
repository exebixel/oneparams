import pandas as pd
from alive_progress import alive_bar
from oneparams.api.cards import ApiCard
from oneparams.api.conta import ApiConta
from oneparams.api.operadora import Operadora
from oneparams.config import CheckException, config_bar
from oneparams.excel.excel import Excel
from oneparams.utils import card_type, print_warning


def cards(book: pd.ExcelFile, header: int = 1, reset: bool = False):
    one = ApiCard()
    print("analyzing spreadsheet")

    ex = Excel(book=book, sheet_name="cart", header_row=header)

    ex.add_column(key="descricao",
                  name="nome",
                  length=100,
                  custom_function_after=check_descricao)
    ex.add_column(key="debito_Credito",
                  name="tipo",
                  custom_function_after=check_debito_credito)
    ex.add_column(key="comissao", name="comissao", default=0, types="float")
    ex.add_column(key="comissaoNegociadaOperadora",
                  name="cobrada",
                  default=0,
                  types="float")
    ex.add_column(key="operadoraCartaoId",
                  name="operadora",
                  default="Padrão",
                  length=50,
                  custom_function_before=check_operadora_before)
    ex.add_column(key="contasId",
                  name="conta",
                  required=False,
                  default="conta corrente",
                  custom_function_after=check_contas)
    ex.clean_columns()

    data_all = ex.data_all(
        checks_final=[check_duplications, resolve_debito_credito])

    operadora = Operadora()
    len_data = len(data_all)
    if reset:
        len_data += len(one.items)
        len_data += len(operadora.items)

    config_bar()
    with alive_bar(len_data) as pbar:
        if reset:
            for i in list(one.items):
                one.delete(i)
                pbar()
            for i in list(operadora.items):
                operadora.delete(i)
                pbar()

        for row in data_all:
            one.diff_item(row)
            pbar()


def check_descricao(value: any, key: str, row: int, default: any) -> str:
    if value is None:
        print(f"ERROR! in line {row}, Column {key}: empty name")
        raise CheckException
    return value


def check_contas(value: any, key: str, row: int, default: any) -> int:
    conta = ApiConta()
    value = conta.submodule_id(value)
    if value is None:
        print(
            f"ERROR! in line {row}, Column {key}: Account '{value}' not found")
        raise CheckException
    return value


def check_debito_credito(value: any, key: str, row: int, default: any) -> int:
    try:
        value = card_type(value)
    except TypeError as exp:
        if value is not None:
            print(f'ERROR! in line {row}, Column {key}: {exp}')
            raise CheckException from exp

        value = "CD"
    return value


def check_operadora_before(value: any, key: str, row: int,
                           default: any) -> any:
    if pd.isnull(value):
        print_warning(
            f"in line {row}, Column {key}: value will be '{default}'")
    return value


def check_duplications(data: pd.DataFrame) -> pd.DataFrame:
    erros = False
    duplic = data[data.duplicated(keep=False,
                                  subset=["descricao", "debito_Credito"])]
    if not duplic.empty:
        erros = True
        duplic.apply(lambda x: print(
            f'ERROR! in line {x["row"]}: Card {x["descricao"]} is duplicated'),
                     axis=1)

    if erros:
        raise CheckException

    return data


def resolve_debito_credito(data: pd.DataFrame) -> pd.DataFrame:
    credito_debito = data.loc[data["debito_Credito"] == "CD"]
    for row in credito_debito.iterrows():
        row = row[1]
        copy = row.copy()
        row["debito_Credito"] = "D"
        copy["debito_Credito"] = "C"
        data = data.append([row, copy])
    data = data[data["debito_Credito"] != "CD"]
    data = data.sort_index()

    return data
