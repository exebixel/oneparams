from api.commission import Commission
from excel.excel import Excel
from utils import get_names


def comissao(book):
    ex = Excel(book, "servico")

    ex.add_column(key="servico", name="nome")
    ex.add_column(key="cols", name="profissionais")

    one = Commission()

    for row in range(2, ex.nrows):
        data = ex.data_row(row)
        if data["cols"] is None:
            continue

        data["cols"] = get_names(data["cols"])

        proc_data = []
        for i in data["cols"]:
            proc_data.append({
                "cols": i,
                "servico": data["servico"],
                "ativo": True
            })
        for i in proc_data:
            one.comissao(i)
