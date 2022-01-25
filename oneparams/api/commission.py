import json

from alive_progress import alive_bar
from oneparams.api.base import BaseApi
from oneparams.api.colaborador import ApiColaboradores
from oneparams.api.servicos import ApiServicos
from oneparams.config import config_bar


class ApiCommission(BaseApi):
    items = {}

    def __init__(self):
        self.cols = ApiColaboradores()
        self.serv = ApiServicos()

    def get_all(self):
        # filtro de colaboradores ativos
        to_get = []
        for cols_id, item in self.cols.items.items():
            if item[self.cols.key_active]:
                to_get.append(cols_id)

        # Gerar a estrutura local com todas as comissões
        config_bar()
        with alive_bar(len(to_get), title="Getting Commission Data") as pbar:
            for cols_id in to_get:
                ApiCommission.items[cols_id] = self.get_servs_in_cols(cols_id)
                pbar()

    def len(self) -> int:
        """ Retorna o número de items salvos em self.items,
        para trazer todas as comissões do sistema,
        é bom executar antes a função self.get_all
        """
        length = 0
        for key in self.items.keys():
            length += len(self.items[key])
        return length

    def get_servs_in_cols(self, cols_id: int) -> dict:
        """ Retorna os serviços realizados por um profissional na api

        cols_id: id do colaborador
        """
        response = self.get(
            f"/OGservsServicosComis/GservsServicosProfissionalRealiza/{cols_id}"
        )
        self.status_ok(response)
        content = json.loads(response.content)

        data = {}
        for i in content["Gservs"]:
            for j in i["Servicos"]:
                data[j["ServicosId"]] = {
                    "servId": j["ServicosId"],
                    "colsId": cols_id,
                }
        return data

    def exist(self, data: dict) -> bool:
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

    def create(self, data: dict) -> None:
        service = self.serv.items[data["servId"]][self.serv.key_name]
        collaborator = self.cols.items[data["colsId"]][self.cols.key_name]
        print(f"adding {service} service to professional {collaborator}")

        response = self.post(
            f"/OServicosComis/AdicionarComissao/{data['colsId']}",
            data=data["servId"])
        self.status_ok(response)

        if data["colsId"] not in self.items:
            ApiCommission.items[data["colsId"]] = {}

        ApiCommission.items[data["colsId"]][data["servId"]] = {
            "colsId": data["colsId"],
            "servId": data["servId"]
        }

    def delete(self, data: dict) -> None:
        service = self.serv.items[data["servId"]][self.serv.key_name]
        collaborator = self.cols.items[data["colsId"]][self.cols.key_name]
        print(f"deleting {service} service in professional {collaborator}")

        response = super().delete(
            f"/Comiservs/RemoverComissao/{data['colsId']}/{data['servId']}")
        self.status_ok(response)

        ApiCommission.items[data["colsId"]].pop(data["servId"])

    def comissao(self, data: dict) -> None:
        if not self.exist(data):
            self.create(data)
        else:
            self.delete(data)
            self.create(data)
