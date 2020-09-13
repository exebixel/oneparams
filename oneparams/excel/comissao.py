from oneparams.api.commission import Commission
from oneparams.excel.excel import Excel
from oneparams.utils import get_names


def comissao(book):
    # Le a tabele de serviços com os profissionais que fazem os serviços
    ex = Excel(book, "servico")
    ex.add_column(key="servico", name="nome")
    ex.add_column(key="ServicoValorComissao",
                  name="comissao",
                  default=0,
                  types="float")
    ex.add_column(key="cols", name="profissionais")

    one = Commission()

    # commdiff = Commdiff(book, one)
    # commdiff.get_data()

    data_all = ex.data_all(check_row=checks_comm)
    for row in data_all:
        one.comissao(row)

        # comm = commdiff.comm_value(i)
        # if (i["ServicoValorComissao"] != comm and comm != -1):
        #     i["ServicoValorComissao"] = comm
        #     one.patch_comissao(i)


def checks_comm(row, data):
    api = Commission()
    if data["cols"] is None:
        return []
    data["cols"] = get_names(data["cols"])

    proc_data = []
    for i in data["cols"]:
        temp = {
            "cols": i,
            "servico": data["servico"],
            "ServicoValorComissao": data["ServicoValorComissao"],
            "ativo": True
        }
        temp = api.change_name_for_id(temp)
        proc_data.append(temp)

    return proc_data


# class Commdiff:
#     def __init__(self, book, api):
#         self.ex = Excel(book, "comiss")
#         self.ex.add_column(key="servico", name="servico")
#         self.ex.add_column(key="cols", name="profissional")
#         self.ex.add_column(key="ServicoValorComissao",
#                            name="comissao",
#                            default=0)
#         self.one = api
#         self.comms = []

#     def get_data(self):
#         print("Analyzing spreadsheet")
#         for row in range(2, self.ex.nrows):
#             data = self.ex.data_row(row)
#             data = self.one.change_name_for_id(data)
#             data.pop("cols")
#             data.pop("servico")
#             self.comms.append(data)

#     def comm_value(self, data):
#         for i in self.comms:
#             if (data["colsId"] == i["colsId"]
#                     and data["servId"] == i["servId"]):
#                 return i["ServicoValorComissao"]
#         return -1
