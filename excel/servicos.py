import xlrd
from datetime import time
from api.servicos import servicos
from api.gservs import gservis
from excel.excel import excel

def servico(book):
    ex = excel(book, "servico")

    ex.add_column("nome", "nome")
    ex.add_column("grupo", "grupo")
    ex.add_column("preco", "valor")
    ex.add_column("comissao", "comissao")
    ex.add_column("tempo_execucao", "execucao")
    one = servicos()

    for row in range(2, ex.nrows):
        data = ex.data_row(row)

        try:
            # convert data
            data["tempo_execucao"] = xlrd.xldate_as_tuple(
                float(data["tempo_execucao"]), book.datemode
            )
            data["tempo_execucao"] = str(
                time(*data["tempo_execucao"][3:])
            )
        except:
            pass

        comissao = float(data["comissao"])
        if comissao <= 1: data["comissao"] = str(comissao * 100)

        one.services(data)

    grupo = gservis()
    grupo.clear()
