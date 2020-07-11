import re, sys
from api.base import base
from utils import *

class comissao(base):

    def __init__(self):
        self.__cols = []

    def get_cols(self):
        response = self.get(
            "/CliForCols/ListaDetalhesColaboradores"
        )
        self.status_ok(response)

        content = json.loads(response.content)
        for i in content:
            if i["ativoColaborador"]:
                self.__cols.append(i)

    def get_cols_id(self, nome):
        nome = deemphasize(nome)
        for i in self.__cols:
            nomeCompleto = deemphasize(i["nomeCompleto"])
            if re.search(nome, nomeCompleto):
                colsId = i["cliForColsId"]

        if len(colsId) == 1:
            return colsId[0]
        else:
            print("collaborator {} not found".format(nome))
            sys.exit()

    def get_serv(self, colsId):
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

    def del(self, colsId, servId):
        response = self.delete(
            "/Comiservs/RemoverComissao/{}/{}".format(colsId, servId)
        )
        self.status_ok(response)
