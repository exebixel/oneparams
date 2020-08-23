from oneparams.api.gservs import Gservis
from oneparams.api.servicos import Servicos
from oneparams.excel.excel import Excel
from oneparams.utils import get_bool


def servico(book):
    ex = Excel(book, "servico")

    ex.add_column(key="descricao", name="nome")
    ex.add_column(key="gserv", name="grupo")
    ex.add_column(key="preco", name="valor", default=0)
    ex.add_column(key="comissao", name="comissao", default=0)
    ex.add_column(key="tempoExecucao", name="execucao", default="00:30:00")
    ex.add_column(key="custosGerais", name="custo", required=False, default=0)
    ex.add_column(key="intervaloMarcacao",
                  name="intervalo",
                  required=False,
                  default="00:10:00")
    ex.add_column(key="permiteEncaixe",
                  name="encaixe",
                  required=False,
                  default=True)
    ex.add_column(key="permiteSimultaneidade",
                  name="simultaniedade",
                  required=False,
                  default=True)
    one = Servicos()

    for row in range(2, ex.nrows):
        data = ex.data_row(row)

        comissao = data["comissao"]
        if comissao <= 1:
            data["comissao"] = comissao * 100

        data["permiteEncaixe"] = get_bool(data["permiteEncaixe"])
        data["permiteSimultaneidade"] = get_bool(data["permiteSimultaneidade"])

        one.diff_item(data)

    grupo = Gservis()
    grupo.clear()
