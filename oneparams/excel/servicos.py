import sys
from typing import Any

from alive_progress import alive_bar
from pandas import ExcelFile
from oneparams.api.gservs import Gservis
from oneparams.api.servicos import ApiServicos
from oneparams.config import CheckException, config_bar_api
from oneparams.excel.excel import Excel


def servico(book: ExcelFile, header: int = 1, reset: bool = False):
    """
    Book: planilha com todos os dados \n
    reset: True se todos os serviços do sistema
    serão excluídos para cadastrar os serviços da planilha \n

    Nessa função tem toda a descrição do json que vai ser enviado
    para as rotas de cadastro do sistema

    Return None
    """
    one = ApiServicos()
    print("analyzing spreadsheet")

    ex = Excel(book, "servico", header_row=header)

    ex.add_column(key="flagAtivo", name="ativo", required=False, default=True)
    ex.add_column(key="descricao",
                  name="nome",
                  length=50,
                  custom_function_after=check_descricao)
    ex.add_column(key="gservId",
                  name="grupo",
                  length=50,
                  custom_function_after=check_descricao)
    ex.add_column(key="preco", name="valor", default=1, types="float")
    ex.add_column(key="comissao",
                  name="comissao",
                  default=0,
                  types="float",
                  custom_function_after=check_comissao)
    ex.add_column(key="tempoExecucao",
                  name="execucao",
                  default="00:30:00",
                  types="time")
    ex.add_column(key="custosGerais",
                  name="custo",
                  required=False,
                  default=0,
                  types="float")
    ex.add_column(key="intervaloMarcacao",
                  name="intervalo",
                  required=False,
                  default="00:10:00",
                  types="time")
    ex.add_column(key="permiteEncaixe",
                  name="encaixe",
                  required=False,
                  default=True,
                  types="bool")
    ex.add_column(key="permiteSimultaneidade",
                  name="simultaneidade",
                  required=False,
                  default=True,
                  types="bool")
    ex.add_column(key="valPercComissao",
                  name="tipo comissao",
                  required=False,
                  default="P")
    ex.add_column(key="valPercCustos",
                  name="tipo custo",
                  required=False,
                  default="P")
    ex.add_column(key="flagMobilidade",
                  name="mobilidade",
                  required=False,
                  default=True,
                  types="bool")
    ex.clean_columns()

    invalid = ex.check_all(check_duplicated_keys=["descricao"])
    if invalid:
        sys.exit(1)

    print("creating services")
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

    with alive_bar() as pbar:
        grupo = Gservis()
        grupo.get_all()
        grupo.clear()


def check_descricao(value: Any, key: str, row: int, default: Any) -> Any:
    if value is None:
        print(f"ERROR! in line {row}, Column {key}, empty value")
        raise CheckException
    return value


def check_comissao(value: Any, key: str, row: int, default: Any) -> float:
    try:
        value = float(value)
    except ValueError as exp:
        raise CheckException from exp

    if value <= 1:
        value = value * 100
    return value
