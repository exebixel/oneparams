from oneparams.api.base_diff import BaseDiff
from oneparams.api.conta import conta
from oneparams.api.operadora import Operadora


class Card(BaseDiff):
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
        self.conta = conta()

    def get_all(self):
        self.items = super().get_all()

    def details(self, item_id):
        return super().details(item_id)["cartoesLight"]

    def item_id(self, data):
        for i in self.items:
            if (i["descricao"] == data["descricao"]
                    and i["debito_Credito"] == data["debito_Credito"]):
                return i["cartoesId"]
        return 0

    def card(self, data):
        if "contasId" not in data.keys():
            data["contasId"] = self.conta.get_id(data["contas"])
            data.pop("contas")
        if "operadoraCartaoId" not in data.keys():
            data["operadoraCartaoId"] = self.operadora.operator(
                data["operadora"])
            data.pop("operadora")

        super().diff_item(data)
