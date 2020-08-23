from oneparams.api.commission import Commission
from oneparams.excel.excel import Excel
from oneparams.utils import get_names


def comissao(book):
    # Le a tabela de comissões diferenciadas
    commdiff = Excel(book, "comiss")
    commdiff.add_column(key="servico", name="servico")
    commdiff.add_column(key="cols", name="profissional")
    commdiff.add_column(key="ServicoValorComissao", name="comissao", default=0)
    comm_data = commdiff.data_all()

    # Le a tabele de serviços com os profissionais que fazem os serviços
    ex = Excel(book, "servico")
    ex.add_column(key="servico", name="nome")
    ex.add_column(key="ServicoValorComissao", name="comissao", default=0)
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
                "cols":
                i,
                "servico":
                data["servico"],
                "ServicoValorComissao":
                data["ServicoValorComissao"],
                "ativo":
                True
            })
        for i in proc_data:
            one.comissao(i)
