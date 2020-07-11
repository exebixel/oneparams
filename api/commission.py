import re, sys
from api.base import base_api
from api.colaborador import colaboradores
from api.servicos import servicos
from utils import *

class commission(base_api):

    def __init__(self):
        self.cols = colaboradores()
        self.serv = servicos()

    def get_servs_in_cols(self, colsId):
        response = self.get(
            "/OGservsServicosComis/GservsServicosProfissionalRealiza/{}".format(colsId),
        )
        self.status_ok(response)
        content = json.loads(response.content)
        data = []
        for i in content["Gservs"]:
            for i in i["Servicos"]:
                data.append({
                    "servId": i["ServicosId"],
                    "servico": i["ServicosNome"],
                    "comissao": i["ServicoValorComissao"],
                    "ativo": i["ServicosAtivo"]
                })
        return data

    def add(self, colsId, servId):
        response = self.post(
            "/OServicosComis/AdicionarComissao/{}".format(colsId),
            data = servId
        )
        self.status_ok(response)

    def delete(self, colsId, servId):
        response = super().delete(
            "/Comiservs/RemoverComissao/{}/{}".format(colsId, servId)
        )
        self.status_ok(response)

    def comissao(self, data):
        data["colsId"] = self.cols.search_item_by_name(data["cols"])
        data.pop("cols")
        data["servId"] = self.serv.item_id(
            {"descricao": data["servico"]})
        data.pop("servico")
        print(data)
