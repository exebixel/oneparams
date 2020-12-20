from oneparams.api.gservs import Gservis
from oneparams.api.servicos import Servicos
from oneparams.excel.excel import Excel
from oneparams.utils import deemphasize


def servico(book, reset=False):
    ex = Excel(book, "servico")

    ex.add_column(key="descricao", name="nome")
    ex.add_column(key="gserv", name="grupo")
    ex.add_column(key="preco", name="valor", default=0, types="float")
    ex.add_column(key="comissao", name="comissao", default=0, types="float")
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
                  name="simultaniedade",
                  required=False,
                  default=True,
                  types="bool")
    one = Servicos()

    print("analyzing spreadsheet")
    data = ex.data_all(check_row=checks)

    if reset:
        one.delete_all()

    for row in data:
        one.diff_item(row)

    grupo = Gservis()
    grupo.all_Gservis()
    grupo.clear()


def checks(row, data, previous):
    erros = False
    if data["descricao"] is None:
        print(f'ERROR! in line {row + 1}: empty name')
        erros = True
    if len(data["descricao"]) > 50:
        print(
            f'ERROR! in line {row + 1}: Service {data["descricao"]} name size {len(data["descricao"])}/50'
        )
        erros = True
    if data["gserv"] is None:
        print(
            f'ERROR! in line {row + 1}: Service {data["descricao"]} have empty group'
        )
        erros = True

    comissao = data["comissao"]
    if comissao <= 1:
        data["comissao"] = comissao * 100

    for prev in previous:
        descricao = deemphasize(data["descricao"])
        prev_descricao = deemphasize(prev["data"]["descricao"])
        if descricao == prev_descricao:
            print(
                f'ERROR! in lines {row + 1} and {prev["row"] +1}: Service {data["descricao"]} is duplicated'
            )
            erros = True

    if erros:
        raise Exception

    one = Servicos()
    return one.name_to_id(data)
