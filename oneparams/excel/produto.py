import sys
from typing import Any
from concurrent.futures import wait
from pebble import ThreadPool
from requests.exceptions import HTTPError

from pandas import DataFrame, ExcelFile
from alive_progress import alive_bar
from oneparams import config
from oneparams.api.produto import ApiProdutos
from oneparams.api.linha_produto import ApiLinhaProduto
from oneparams.api.grupo_produto import ApiGrupoProduto
from oneparams.api.fabricante import ApiFabricante
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
    ex.add_column(key="gruposId",
                  name="grupo",
                  length=100,
                  default="Padrão",
                  custom_function_before=check_linha_before)
    ex.add_column(key="linhasId",
                  name="linha",
                  length=100,
                  default="Padrão",
                  custom_function_before=check_linha_before)
    ex.add_column(key="estoqueMinimo",
                  name=["estoque", "minimo"],
                  default=0,
                  types="int")
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

    ex.add_column(key="aliquotaIcms",
                  name=["aliquota", "icms"],
                  types="float",
                  required=False)
    ex.add_column(key="baseCalcIcms",
                  name=["base", "icms"],
                  types="float",
                  required=False)
    ex.add_column(key="icmsEcf",
                  name=["icms", "ecf"],
                  types="float",
                  required=False)
    ex.add_column(key="ncm", name="ncm", types="int", required=False)
    ex.add_column(key="substTributaria",
                  name=["subst", "tributaria"],
                  types="bool",
                  required=False)
    ex.add_column(key="lucroSubstTributaria",
                  name=["lucro", "subst", "tributaria"],
                  types="float",
                  required=False)
    ex.add_column(key="codTributario",
                  name=["codigo", "tributario"],
                  types="int",
                  required=False)
    ex.add_column(key="cfop", name="cfop", length=50, required=False)
    ex.add_column(key="cst", name="cst", types="int", required=False)
    ex.add_column(key="csosn", name="csosn", types="int", required=False)
    ex.add_column(key="cstTributariaPis",
                  name=["cst", "pis"],
                  types="int",
                  required=False)
    ex.add_column(key="aliquotaPis",
                  name=["aliquota", "pis"],
                  types="float",
                  required=False)
    ex.add_column(key="cstTributariaCofins",
                  name=["cst", "cofins"],
                  types="int",
                  required=False)
    ex.add_column(key="aliquotaCofins",
                  name=["aliquota", "cofins"],
                  types="float",
                  required=False)
    ex.add_column(key="cest", name="cest", length=40, required=False)

    ex.clean_columns()

    invalid = ex.check_all(check_duplicated_keys=["descricao"],
                           checks_final=[skip_items])
    if invalid:
        sys.exit(1)

    print("creating products")
    data = ex.data_all()

    api_grupo = ApiGrupoProduto()
    api_linha = ApiLinhaProduto()
    api_fabricante = ApiFabricante()

    len_data = len(data)
    linhas = []
    grupos = []
    fabricantes = []
    for i in data:
        if (i["linhasId"] not in linhas and api_linha.item_id(
            {api_linha.key_name: i["linhasId"]}) == 0):
            linhas.append(i["linhasId"])
        if (i["gruposId"] not in grupos and api_grupo.item_id(
            {api_grupo.key_name: i["gruposId"]}) == 0):
            grupos.append(i["gruposId"])
        if (i["fabricantesId"] not in fabricantes and api_fabricante.item_id(
            {api_fabricante.key_name: i["fabricantesId"]}) == 0):
            fabricantes.append(i["fabricantesId"])
    len_data += len(linhas) + len(grupos) + len(fabricantes)

    if reset:
        len_data += len(one.items)

    config_bar_api()
    with alive_bar(len_data) as pbar:
        with ThreadPool(max_workers=config.MAX_THREADS) as pool:

            def result_item(future):
                try:
                    future.result()
                    pbar()
                except HTTPError as exp:
                    print(exp)
                    pool.stop()
                except Exception as exp:
                    print(f"ERROR! {exp}")
                    pool.stop()

            queues = []
            if reset:
                for item in list(one.items):
                    future = pool.submit(one.delete, item)
                    future.add_done_callback(result_item)
                    queues.append(future)
                results = wait(queues, return_when="FIRST_EXCEPTION")
                if results.not_done:
                    pool.stop()
                    sys.exit(1)

            queues = []
            for item in linhas:
                future = pool.submit(api_linha.submodule_id, item)
                future.add_done_callback(result_item)
                queues.append(future)
            for item in grupos:
                future = pool.submit(api_grupo.submodule_id, item)
                future.add_done_callback(result_item)
                queues.append(future)
            for item in fabricantes:
                future = pool.submit(api_fabricante.submodule_id, item)
                future.add_done_callback(result_item)
                queues.append(future)
            results = wait(queues, return_when="FIRST_EXCEPTION")
            if results.not_done:
                pool.stop()
                sys.exit(1)

            queues = []
            for item in data:
                future = pool.submit(one.diff_item, item)
                future.add_done_callback(result_item)
                queues.append(future)
            results = wait(queues, return_when="FIRST_EXCEPTION")
            if results.not_done:
                pool.stop()
                sys.exit(1)


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
