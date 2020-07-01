import xlrd
from api.servicos import servicos
from api.gservs import gservis
from excel.excel import excel

def servico(book):
    ex = excel(book, "servico")

    ex.add_column("descricao", "nome")
    ex.add_column("gserv", "grupo")
    ex.add_column("preco", "valor", 
                  default=0)
    ex.add_column("comissao", "comissao",
                  default=0)
    ex.add_column("tempoExecucao", "execucao",
                  default="00:30:00")
    ex.add_column(key="intervaloMarcacao", name="intervalo",
                  required=False, default="00:10:00")
    ex.add_column(key="permiteEncaixe", name="excaixe",
                  required=False, default=True)
    ex.add_column(key="permiteSimultaneidade", name="simultanidade",
                  required=False, default=True)
    one = servicos()

    for row in range(2, ex.nrows):
        data = ex.data_row(row)

        comissao = data["comissao"]
        if comissao <= 1: data["comissao"] = comissao * 100

        one.services(data)

    grupo = gservis()
    grupo.clear()
