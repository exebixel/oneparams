from oneparams.api.base_diff import BaseDiff
from oneparams.api.conta import Conta
from oneparams.api.operadora import Operadora


class apiCard(BaseDiff):
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
                         url_delete="/Cartoes",
                         submodules={
                             "contas": Conta(),
                             "operadoraCartao": Operadora()
                         })

        # self.operadora = Operadora()
        # self.conta = Conta()
        if not apiCard.first_get:
            self.get_all()
            apiCard.first_get = True

    def get_all(self):
        apiCard.items = super().get_all()

    def details(self, item_id):
        return super().details(item_id)["cartoesLight"]

    def item_id(self, data):
        for i in apiCard.items:
            if (i["descricao"] == data["descricao"]
                    and i["debito_Credito"] == data["debito_Credito"]):
                return i["cartoesId"]
        return 0
