import sys
from typing import Any

from pandas import ExcelFile, isnull
from alive_progress import alive_bar
from oneparams.api.colaborador import ApiColaboradores
from oneparams.config import CheckException, config_bar_api
from oneparams.excel.excel import Excel
from oneparams.utils import print_warning


def colaborador(book: ExcelFile, header: int = 1):
    one = ApiColaboradores()
    print("analyzing spreadsheet")

    ex = Excel(book=book, sheet_name="profissiona", header_row=header)

    ex.add_column(key="nomeCompleto",
                  name="nome",
                  length=50,
                  custom_function_after=checks_nome_completo)
    ex.add_column(key="email", name="email", types="email", length=50)
    ex.add_column(key="celular", name="celular", types="cel")
    ex.add_column(key="perfilId",
                  name="perfil",
                  default="colaborador",
                  custom_function_before=checks_perfil)
    ex.add_column(key="agendavel",
                  name="agenda",
                  required=False,
                  default=False,
                  types="bool")
    ex.add_column(key="profissaoId",
                  name="profissao",
                  required=False,
                  default=None)
    ex.add_column(key="flagCliente",
                  name="cliente",
                  required=False,
                  default=True,
                  types="bool")
    ex.add_column(key="flagFornecedor",
                  name="fornecedor",
                  required=False,
                  default=True,
                  types="bool")
    ex.add_column(key="agendavelMobilidade",
                  name="mobilidade",
                  required=False,
                  default=True,
                  types="bool")
    ex.clean_columns()

    invalid = ex.check_all(
        check_row=checks_row,
        check_duplicated_keys=["nomeCompleto", "email", "celular"])
    if invalid:
        sys.exit(1)

    print("creating collaborators")
    data = ex.data_all()
    len_data = len(data)

    config_bar_api()
    with alive_bar(len_data) as pbar:
        for row in data:
            one.diff_item(row)
            pbar()


def checks_nome_completo(value: Any, key: str, row: int, default: Any) -> str:
    if value is None:
        print(f"ERROR! in line {row}, Column {key}: empty name")
        raise CheckException
    return value


def checks_perfil(value: Any, key: str, row: int, default: Any) -> str:
    if isnull(value):
        print_warning(
            f"In line {row}, Column {key}: value will be '{default}'")
    return value


def checks_row(row: int, data: dict) -> dict:
    one = ApiColaboradores()
    try:
        data = one.name_to_id(data)
    except ValueError as exp:
        for i in exp.args:
            print(f'ERROR! in line {row}: {i}')
        raise CheckException from exp

    return data
