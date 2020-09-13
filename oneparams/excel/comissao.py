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

    data_all = ex.data_all(check_row=checks_comm)
    for row in data_all:
        one.comissao(row)


def checks_comm(row, data):
    erros = False
    api = Commission()

    data["servId"] = api.serv.item_id({"descricao": data["servico"]})
    if data["servId"] == 0:
        print("ERROR!! in line {}: Service {} not found".format(
            row + 1, data["servico"]))
        erros = True

    if data["cols"] is None:
        return []
    data["cols"] = get_names(data["cols"])

    colsId = []
    for i in data["cols"]:
        cols = {}
        cols["name"] = i
        try:
            cols["id"] = api.cols.search_item_by_name(cols["name"])
        except ValueError as exp:
            print("ERROR!! in line {}: {}".format(row + 1, exp))
            erros = True
        else:
            colsId.append(cols)
    data["cols"] = colsId

    proc_data = []
    for i in data["cols"]:
        temp = {
            "cols": i["name"],
            "colsId": i["id"],
            "servico": data["servico"],
            "servId": data["servId"],
            "ServicoValorComissao": data["ServicoValorComissao"],
            "ativo": True
        }
        proc_data.append(temp)

    if erros:
        raise Exception
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
