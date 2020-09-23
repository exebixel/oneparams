from oneparams.api.base_diff import BaseDiff
from oneparams.api.conta import Conta
from oneparams.api.operadora import Operadora


class Card(BaseDiff):
    items = []
    first_get = False

    def __init__(self):
        super().__init__(key_id="cartoesId",
                         key_name="descricao",
                         item_name="card",
                         url_create="/OCartao/Cartoes",
                         url_update="/OCartao/Cartoes",
                         url_get_all="/Cartoes",
                         url_get_detail="/OCartao/CartaoDetalhes",
                         url_delete="/Cartoes")

        self.operadora = Operadora()
        self.conta = Conta()
        if not Card.first_get:
            self.get_all()
            Card.first_get = True

    def get_all(self):
        Card.items = super().get_all()

    def details(self, item_id):
        return super().details(item_id)["cartoesLight"]

    def item_id(self, data):
        for i in Card.items:
            if (i["descricao"] == data["descricao"]
                    and i["debito_Credito"] == data["debito_Credito"]):
                return i["cartoesId"]
        return 0

    def name_to_id(self, data):
        if "contasId" not in data.keys():
            data["contasId"] = self.conta.get_id(data["contas"])
            data.pop("contas")
        if "operadoraCartaoId" not in data.keys():
            data["operadoraCartaoId"] = self.operadora.operator(
                data["operadora"])
            data.pop("operadora")
        return data

    def card(self, data):
        data = self.name_to_id(data)
        super().diff_item(data)
