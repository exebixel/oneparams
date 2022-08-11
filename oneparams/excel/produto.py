import sys
from typing import Any

from pandas import DataFrame, ExcelFile
from alive_progress import alive_bar
from oneparams import config
from oneparams.api.produto import ApiProdutos
from oneparams.config import CheckException, config_bar_api
from oneparams.excel.excel import Excel
from oneparams.utils import print_warning


def produtos(book: ExcelFile, header: int = 1, reset: bool = False):

    one = ApiProdutos()
    print("analyzing spreadsheet")

    ex = Excel(book, "produto", header_row=header, verbose=True)

    ex.add_column(key="ativo", name="ativo", required=False, default=True)
    ex.add_column(key="descricao",
                  name="nome",
                  length=50,
                  custom_function_after=check_descricao)
    ex.add_column(key="fabricantesId",
                  name="fabricante",
                  length=50,
                  default="Padrão",
                  custom_function_before=check_fabricante_before)
    ex.add_column(key="linhasId",
                  name="linha",
                  length=50,
                  default="Padrão",
                  custom_function_before=check_linha_before)
    ex.add_column(key="estoqueMinimo", name="estoque", default=0, types="int")
    ex.add_column(key="codigoBarras", name="codigo", length=20)
    ex.add_column(key="precoVenda",
                  name=["preco", "cliente"],
                  default=0,
                  types="float")
    ex.add_column(key="comissaoVenda",
                  name=["comissao", "cliente"],
                  default=0,
                  types="float")
    ex.add_column(key="precoColaborador",
                  name=["preco", "colaborador"],
                  default=0,
                  types="float")
    ex.add_column(key="comissaoColaborador",
                  name=["comissao", "colaborador"],
                  default=0,
                  types="float")

    ex.clean_columns()

    invalid = ex.check_all(check_duplicated_keys=["descricao"],
                           checks_final=[skip_items])
    if invalid:
        sys.exit(1)

    print("creating products")
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


def check_descricao(value: str, key: str, row: int, default: Any) -> str:
    if value is None:
        print(f"ERROR! in line {row}, Column {key}, empty value")
        raise CheckException
    return value


def check_fabricante_before(value: str, key: str, row: int,
                            default: Any) -> str:
    if value is None:
        print_warning(
            f"in line {row}, Column {key}, value will be '{default}'")
    return value


def check_linha_before(value: str, key: str, row: int, default: Any) -> str:
    if value is None:
        print_warning(
            f"in line {row}, Column {key}, value will be '{default}'")
    return value


def skip_items(data: DataFrame):
    if not config.SKIP:
        return data

    one = ApiProdutos()
    with alive_bar(len(data),
                   receipt=True,
                   title="Skiping registered products...") as pbar:
        for prod in one.items.values():
            data = data.drop(
                data[data["descricao"] == prod["descricao"]].index)
            pbar()

    return data
