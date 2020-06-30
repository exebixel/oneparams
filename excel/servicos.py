import xlrd
from datetime import time
from api.servicos import servicos
from api.gservs import gservis
from excel.excel import excel

def servico(book):
    ex = excel(book, "servico")

    ex.add_column("descricao", "nome")
    ex.add_column("gserv", "grupo")
    ex.add_column("preco", "valor")
    ex.add_column("comissao", "comissao")
    ex.add_column("tempoExecucao", "execucao")
    one = servicos()

    for row in range(2, ex.nrows):
        data = ex.data_row(row)

        try:
            # convert data
            data["tempoExecucao"] = xlrd.xldate_as_tuple(
                float(data["tempoExecucao"]), book.datemode
            )
            data["tempoExecucao"] = str(
                time(*data["tempoExecucao"][3:])
            )
        except:
            pass

        comissao = float(data["comissao"])
        if comissao <= 1: data["comissao"] = str(comissao * 100)

        one.services(data)

    grupo = gservis()
    grupo.clear()
