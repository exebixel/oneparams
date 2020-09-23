from oneparams.api.gservs import Gservis
from oneparams.api.servicos import Servicos
from oneparams.excel.excel import Excel


def servico(book):
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
    for row in data:
        one.diff_item(row)

    grupo = Gservis()
    grupo.all_Gservis()
    grupo.clear()


def checks(row, data):
    erros = False
    if data["descricao"] is None:
        print("ERROR! in line {}: empty name".format(row + 1))
        erros = True
    if data["gserv"] is None:
        print("ERROR! in line {}: empty group".format(row + 1))
        erros = True

    comissao = data["comissao"]
    if comissao <= 1:
        data["comissao"] = comissao * 100

    if erros:
        raise Exception

    one = Servicos()
    return one.name_to_id(data)
