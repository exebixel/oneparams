from oneparams.api.commission import Commission
from oneparams.excel.excel import Excel
from oneparams.utils import get_names


def comissao(book):
    # Le a tabele de serviços com os profissionais que fazem os serviços
    ex = Excel(book, "servico")
    ex.add_column(key="servico", name="nome")
    ex.add_column(key="ServicoValorComissao", name="comissao", default=0)
    ex.add_column(key="cols", name="profissionais")

    one = Commission()

    commdiff = Commdiff(book, one)
    commdiff.get_data()

    for row in range(2, ex.nrows):
        data = ex.data_row(row)
        if data["cols"] is None:
            continue

        for i in separate_names(data):
            i = one.change_name_for_id(i)
            one.comissao(i)

            comm = commdiff.comm_value(i)
            if (i["ServicoValorComissao"] != comm and comm != -1):
                i["ServicoValorComissao"] = comm
                one.patch_comissao(i)


def separate_names(data):
    data["cols"] = get_names(data["cols"])

    proc_data = []
    for i in data["cols"]:
        proc_data.append({
            "cols": i,
            "servico": data["servico"],
            "ServicoValorComissao": data["ServicoValorComissao"],
            "ativo": True
        })
    return proc_data


class Commdiff:
    def __init__(self, book, api):
        self.ex = Excel(book, "comiss")
        self.ex.add_column(key="servico", name="servico")
        self.ex.add_column(key="cols", name="profissional")
        self.ex.add_column(key="ServicoValorComissao",
                           name="comissao",
                           default=0)
        self.one = api
        self.comms = []

    def get_data(self):
        print("Analyzing spreadsheet")
        for row in range(2, self.ex.nrows):
            data = self.ex.data_row(row)
            data = self.one.change_name_for_id(data)
            data.pop("cols")
            data.pop("servico")
            self.comms.append(data)

    def comm_value(self, data):
        for i in self.comms:
            if (data["colsId"] == i["colsId"]
                    and data["servId"] == i["servId"]):
                return i["ServicoValorComissao"]
        return -1
