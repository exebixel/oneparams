from pandas import DataFrame, ExcelFile
from alive_progress import alive_bar
from oneparams.api.gservs import Gservis
from oneparams.api.servicos import ApiServicos
from oneparams.config import CheckException, config_bar
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
    ex.clean_columns()

    data = ex.data_all(checks_final=[check_duplications])

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

    with alive_bar() as pbar:
        grupo = Gservis()
        grupo.get_all()
        grupo.clear()


def check_descricao(value: any, key: str, row: int, default: any) -> any:
    if value is None:
        print(f"ERROR! in line {row}, Column {key}, empty value")
        raise CheckException
    return value


def check_comissao(value: any, key: str, row: int, default: any) -> any:
    if value <= 1:
        value = value * 100
    return value


def check_duplications(data: DataFrame) -> DataFrame:
    """
    self: referencia da classe excel \n
    data: data frame com todos os dados da planilha \n

    Verificações 'globais', que necessitam de todos os
    dados da planilha, principalmente duplicações

    return data \n
    raise Exception: caso tenha algum erro durante as
    verificações \n

    """
    erros = False
    duplic = data[data.duplicated(keep=False, subset=["descricao"])]
    for i in duplic.index:
        for j in duplic.index:
            if (duplic.loc[i, "descricao"] == duplic.loc[j, "descricao"]
                    and j != i):
                print("ERROR! in lines {} and {}: Service {} is duplicated".
                      format(duplic.loc[i, 'row'], duplic.loc[j, 'row'],
                             duplic.loc[i, 'descricao']))
                duplic = duplic.drop(index=i)
                erros = True
                break
    if erros:
        raise CheckException

    return data
