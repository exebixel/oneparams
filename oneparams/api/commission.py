import json

from oneparams.api.base import BaseApi
from oneparams.api.colaborador import Colaboradores
from oneparams.api.servicos import Servicos


class Commission(BaseApi):
    def __init__(self):
        self.cols = Colaboradores()
        self.serv = Servicos()
        self.items = []

    def get_servs_in_cols(self, colsId):
        response = self.get(
            "/OGservsServicosComis/GservsServicosProfissionalRealiza/{}".
            format(colsId), )
        self.status_ok(response)
        content = json.loads(response.content)
        data = {}
        data["colsId"] = colsId
        data["servs"] = []
        for i in content["Gservs"]:
            for i in i["Servicos"]:
                data["servs"].append({
                    "servId": i["ServicosId"],
                    "serv": i["ServicosNome"],
                    "comissao": i["ServicoValorComissao"],
                })
        return data

    def index_cols(self, colsId):
        index = 0
        for i in self.items:
            if (i["colsId"] == colsId):
                return index
            index += 1
        return -1

    def exist(self, data):
        index = self.index_cols(data["colsId"])
        if index == -1:
            item = self.get_servs_in_cols(data["colsId"])
            self.items.append(item)
        else:
            item = self.items[index]

        for i in item["servs"]:
            if i["servId"] == data["servId"]:
                return True
        return False

    def add(self, data):
        response = self.post("/OServicosComis/AdicionarComissao/{}".format(
            data["colsId"]),
                             data=data["servId"])
        self.status_ok(response)

    def delete(self, data):
        response = super().delete("/Comiservs/RemoverComissao/{}/{}".format(
            data["colsId"], data["servId"]))
        self.status_ok(response)

    def delete_all(self):
        cols = self.cols.items
        for cols in cols:
            data = self.get_servs_in_cols(cols["colaboradorId"])
            for i in data["servs"]:
                print("deleting {} service in professional {}".format(
                    i["serv"], cols["nomeCompleto"]))
                self.delete({
                    "colsId": cols["colaboradorId"],
                    "servId": i["servId"]
                })

    def change_name_for_id(self, data):
        erros = []
        if "cols" in data.keys():
            try:
                data["colsId"] = self.cols.search_item_by_name(data["cols"])
            except ValueError as exp:
                erros.append(str(exp))
        if "servico" in data.keys():
            data["servId"] = self.serv.item_id({"descricao": data["servico"]})
            if data["servId"] == 0:
                erros.append("Service {} not found".format(data["servico"]))

        if erros != []:
            raise Exception(erros)
        return data

    def comissao(self, data):
        data = self.change_name_for_id(data)

        if not self.exist(data):
            print("adding {} service to professional {}".format(
                data["servico"], data["cols"]))
            self.add(data)
        else:
            print("updating {} service to professional {}".format(
                data["servico"], data["cols"]))
            self.delete(data)
            self.add(data)

    def patch_comissao(self, data):
        print("applying differentiated commission")
        if "servId" in data.keys():
            data["ServicosId"] = data["servId"]
            data.pop("servId")
        response = self.patch(
            "/Comiservs/ComiservsLight/{}".format(data["colsId"]), data)
        self.status_ok(response)
