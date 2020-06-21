import json
from api.base import base_api
from api.operadora import operadora
from api.conta import conta

class card(base_api):

    def __init__(self):
        self.__cards = []
        self.all_cards()
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
        card = content["cartoesLight"]
        return {
            "descricao": card["descricao"],
            "debito_Credito": card["debito_Credito"],
            "comissao": card["comissao"],
            "comissaoNegociadaOperadora": card["comissaoNegociadaOperadora"],
            "operadora": content["operadoraCartoesPesquisa"]["descricao"],
            "operadoraCartaoId": card["operadoraCartaoId"]
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

    def update(self, data):
        card_id = self.get_id(data["descricao"])
        data["cartoesId"] = card_id
        data["operadoraCartaoId"] = self.operadora.operator(data["operadora"])
        data["contasId"] = self.conta.get_id("conta corrente")

        print("updating {} card".format(data["descricao"]))
        response = self.put("/OCartao/Cartoes/{}".format(card_id), data)
        self.status_ok(response)


    def equals(self, data):
        detalis = self.details(data["descricao"])
        keys = data.keys()
        cont = 0
        for key in keys:
            if data[key] == str(detalis[key]):
                cont += 1
        if cont == len(data):
            return True
        return False
