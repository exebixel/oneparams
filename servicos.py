import xlrd
from  datetime import time
from one_api import one_api
from excel_class import excel

def servico(book, access_token):
    sheet_name = "servico"
    sh_index = excel.sheet_index(book, sheet_name)
    if sh_index == -1:
        print("sheet {0} not found!".format(sheet_name))
        exit()

    sh = book.sheet_by_index(sh_index)

    nome_index = excel.column_index(sh, "descricao")
    grupo_index = excel.column_index(sh, "grupo")
    preco_index = excel.column_index(sh, "valor")
    comissao_index = excel.column_index(sh, "comissao")
    execucao_index = excel.column_index(sh, "execucao")

    one = one_api(access_token)

    for row in range(1, sh.nrows):
        nome_value = sh.cell_value(rowx=row, colx=nome_index)
        preco_value = sh.cell_value(rowx=row, colx=preco_index)
        comissao_value = sh.cell_value(rowx=row, colx=comissao_index)
        gservs_value = sh.cell_value(rowx=row, colx=grupo_index)

        tempo_execucao = sh.cell_value(rowx=row, colx=execucao_index)
        try:
            # convert data
            tempo_execucao = xlrd.xldate_as_tuple(tempo_execucao, book.datemode)
            tempo_execucao = str( time(*tempo_execucao[3:]) )
        except TypeError:
            pass


        one.services(
            nome = nome_value,
            preco = preco_value,
            comissao = comissao_value,
            tempoExecucao = tempo_execucao,
            gservs = gservs_value
        )
