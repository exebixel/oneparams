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
        # nome_value = sh.cell_value(rowx=row, colx=nome_index).strip()
        # preco_value = sh.cell_value(rowx=row, colx=preco_index)
        # comissao_value = sh.cell_value(rowx=row, colx=comissao_index)
        # gservs_value = sh.cell_value(rowx=row, colx=grupo_index).strip()
        data = ex.data_row(row)

        # tempo_execucao = sh.cell_value(rowx=row, colx=execucao_index)
        try:
            # convert data
            data["tempo_execucao"] = xlrd.xldate_as_tuple(
                float(data["tempo_execucao"]), book.datemode
            )
            data["tempo_execucao"] = str(
                time(*data["tempo_execucao"][3:])
            )
        except TypeError:
            pass

        # data = {
        #     "nome":  nome_value,
        #     "preco":  preco_value,
        #     "comissao":  comissao_value,
        #     "tempo_execucao":  tempo_execucao,
        #     "grupo":  gservs_value
        # }
        one.services(data)

    grupo = gservis()
    grupo.clear()
