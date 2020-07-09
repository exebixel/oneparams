import json
from api.base_diff import base_diff
from api.operadora import operadora
from api.conta import conta

class card(base_diff):

    def __init__(self):
        super().__init__(
            key_id = "cartoesId",
            key_name = "descricao",
            item_name = "card",

            url_create = "/OCartao/Cartoes",
            url_update = "/OCartao/Cartoes",
            url_get_all = "/Cartoes",
            url_get_detail = "/OCartao/CartaoDetalhes",

            url_delete = "/Cartoes"
        )

        self.operadora = operadora()
        self.conta = conta()

    def get_all(self):
        content = super().get_all()
        for i in content:
            self.items.append(i)

    def details(self, item_id):
        return super().details(item_id)["cartoesLight"]

    def card(self, data):
        data["contasId"] = self.conta.get_id(data["contas"])
        data.pop("contas")
        data["operadoraCartaoId"] = self.operadora.operator(data["operadora"])
        data.pop("operadora")

        super().diff_item(data)
