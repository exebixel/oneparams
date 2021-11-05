import json

from alive_progress import alive_bar
from oneparams.config import config_bar

from oneparams.api.base import BaseApi
from oneparams.api.colaborador import ApiColaboradores
from oneparams.api.servicos import ApiServicos


class ApiCommission(BaseApi):
    items = {}

    def __init__(self):
        self.cols = ApiColaboradores()
        self.serv = ApiServicos()

    def get_all(self):
        # filtro de colaboradores ativos
        to_get = []
        for colsId, item in self.cols.items.items():
            if item[self.cols.key_active] == True:
                to_get.append(colsId)

        # Gerar a estrutura local com todas as comissões
        config_bar()
        with alive_bar(len(to_get), title="Getting Commission Data") as bar:
            for colsId in to_get:
                ApiCommission.items[colsId] = self.get_servs_in_cols(colsId)
                bar()

    def len(self):
        length = 0
        for key in self.items.keys():
            length += len(self.items[key])
        return length


    def get_servs_in_cols(self, colsId):
        response = self.get(
            "/OGservsServicosComis/GservsServicosProfissionalRealiza/{}".
            format(colsId), )
        self.status_ok(response)
        content = json.loads(response.content)

        data = {}
        for i in content["Gservs"]:
            for i in i["Servicos"]:
                data[i["ServicosId"]] = {
                    "servId": i["ServicosId"],
                    "colsId": colsId,
                }
        return data

    def exist(self, data):
        try:
            if data["servId"] in ApiCommission.items[data["colsId"]]:
                return True
        except KeyError:
            servs = self.get_servs_in_cols(data["colsId"])
            ApiCommission.items[data["colsId"]] = servs
            if data["servId"] in servs:
                return True
            return False
        return False

    def create(self, data):
        print("adding {} service to professional {}".format(
            self.serv.items[data["servId"]][self.serv.key_name],
            self.cols.items[data["colsId"]][self.cols.key_name]
        ))

        response = self.post("/OServicosComis/AdicionarComissao/{}".format(
            data["colsId"]),
            data=data["servId"])
        self.status_ok(response)

        if data["colsId"] not in self.items:
            ApiCommission.items[data["colsId"]] = {}
        ApiCommission.items[data["colsId"]][data["servId"]] = {
            "colsId": data["colsId"],
            "servId": data["servId"]
        }

    def delete(self, data):
        print("deleting {} service in professional {}".format(
            self.serv.items[data["servId"]][self.serv.key_name],
            self.cols.items[data["colsId"]][self.cols.key_name]
        ))

        response = super().delete("/Comiservs/RemoverComissao/{}/{}".format(
            data["colsId"], data["servId"]))
        self.status_ok(response)

        ApiCommission.items[data["colsId"]].pop(data["servId"])

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
        # data = self.change_name_for_id(data)

        if not self.exist(data):
            self.create(data)
        else:
            self.delete(data)
            self.create(data)
