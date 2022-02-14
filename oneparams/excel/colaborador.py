import pandas as pd
from alive_progress import alive_bar
from oneparams.api.colaborador import ApiColaboradores
from oneparams.config import CheckException, config_bar
from oneparams.excel.excel import Excel
from oneparams.utils import print_warning


def colaborador(book: pd.ExcelFile, header: int = 1):
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

    data = ex.data_all(check_row=checks, checks_final=[check_duplications])
    len_data = len(data)

    config_bar()
    with alive_bar(len_data) as pbar:
        for row in data:
            one.diff_item(row)
            pbar()


def checks_nome_completo(value: any, key: str, row: int, default: any) -> str:
    if value is None:
        print(f"ERROR! in line {row}, Column {key}: empty name")
        raise CheckException
    return value


def checks_perfil(value: any, key: str, row: int, default: any) -> str:
    if pd.isnull(value):
        print_warning(
            f"In line {row}, Column {key}: value will be '{default}'")
    return value


def checks(row: int, data: dict) -> dict:
    one = ApiColaboradores()
    try:
        data = one.name_to_id(data)
    except ValueError as exp:
        for i in exp.args:
            print(f'ERROR! in line {row}: {i}')
        raise CheckException from exp

    return data


def check_duplications(data: pd.DataFrame) -> pd.DataFrame:
    erros = False
    cols = {
        "nomeCompleto":
        "ERROR! in lines {} and {}: Collaborator '{}' is duplicated",
        "email":
        "ERROR! in lines {} and {}: Collaborator\'s email '{}' is duplicated",
        "celular":
        "ERROR! in lines {} and {}: Collaborator phone '{}' is duplicated"
    }
    for col, print_erro in cols.items():
        duplic = data[data.duplicated(keep=False, subset=col)]
        for i in duplic.loc[data[col].notnull()].index:
            for j in duplic.loc[data[col].notnull()].index:
                if (duplic.loc[i, col] == duplic.loc[j, col] and j != i):
                    print(
                        print_erro.format(duplic.loc[i, 'row'],
                                          duplic.loc[j, 'row'],
                                          duplic.loc[i, col]))
                    duplic = duplic.drop(index=i)
                    erros = True
                    break
    if erros:
        raise CheckException

    return data
