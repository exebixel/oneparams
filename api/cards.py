import json
from api.base import base_api
from api.operadora import operadora
from api.conta import conta

class card(base_api):

    def __init__(self):
        self.__cards = []
        self.operadora = operadora()
        self.conta = conta()

    def all_cards(self):
        response = self.get("/Cartoes")
        self.status_ok(response)

        print("researching cards")
        content = json.loads(response.content)
        for i in content:
            self.__cards.append({
                "cartoesId": i["cartoesId"],
                "descricao": i["descricao"],
                "debito_Credito": i["debito_Credito"]
            })

    def get_id(self, nome):
        for i in self.__cards:
            if i["descricao"] == nome:
                return i["cartoesId"]
        return None

    def details(self, nome):
        card_id = self.get_id(nome)
        response = self.get("/OCartao/CartaoDetalhes/{}".format(card_id))
        self.status_ok(response)

        content = json.loads(response.content)
        return {
            "descricao": content["descricao"],
            "debito_Credito": content["debito_Credito"],
            "comissao": content["comissao"],
            "comissaoNegociadaOperadora": content["comissaoNegociadaOperadora"],
            "operadora": content["operadora"],
            "operadoraCartaoId": content["operadoraCartaoId"]
        }

    def create(self, data):
        data["operadoraCartaoId"] = self.operadora.operator(data["operadora"])
        data["contasId"] = self.conta.get_id("conta corrente")
        print("creating {} card".format(data["descricao"]))
        response = self.post("/OCartao/Cartoes", data)
        self.status_ok(response)

        content = json.loads(response.content)
        data["cartoesId"] = content["data"]
        self.__cards.append(data)
