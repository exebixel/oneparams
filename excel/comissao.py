from excel.excel import excel
from utils import *

def comissao(book):
    ex = excel(book, "servico")

    ex.add_column(key="servico", name="nome")
    ex.add_column(key="cols", name="profissionais")

    for row in range(2, ex.nrows):
        data = ex.data_row(row)
        data["cols"] = get_names(data["cols"])

        proc_data = []
        for i in data["profissional"]:
            proc_data.append({
                "cols": i,
                "servico": data["ServicosNome"],
                "ativo": True
            })
        print(proc_data)
