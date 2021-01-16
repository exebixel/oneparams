from oneparams.api.base_diff import BaseDiff
from oneparams.api.conta import Conta
from oneparams.api.operadora import Operadora


class apiCard(BaseDiff):
    items = []
    list_details = []
    first_get = False

    def __init__(self):
        super().__init__(key_id="cartoesId",
                         key_name="descricao",
                         item_name="card",
                         url_create="/OCartao/Cartoes",
                         url_update="/OCartao/Cartoes",
                         url_get_all="/Cartoes",
                         url_get_detail="/OCartao/CartaoDetalhes",
                         key_detail="cartoesLight",
                         url_delete="/Cartoes",
                         submodules={
                             "contasId": Conta(),
                             "operadoraCartaoId": Operadora()
                         })

        if not apiCard.first_get:
            self.get_all()
            apiCard.first_get = True

    def get_all(self):
        apiCard.items = super().get_all()

    def item_id(self, data):
        for i in apiCard.items:
            if (i["descricao"] == data["descricao"]
                    and i["debito_Credito"] == data["debito_Credito"]):
                return i["cartoesId"]
        return 0
