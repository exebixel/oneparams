from excel.excel import excel
from utils import *

def comissao(book):
    ex = excel(book, "servico")

    ex.add_column(key="ServicosNome", name="nome")
    ex.add_column(key="profissional", name="profissionais")

    for row in range(2, ex.nrows):
        data = ex.data_row(row)
        data["profissional"] = get_names(data["profissional"])
        print(data)
