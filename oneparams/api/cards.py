from oneparams.api.base_diff import BaseDiff
from oneparams.api.conta import Conta
from oneparams.api.operadora import Operadora


class apiCard(BaseDiff):
    items = {}
    list_details = {}
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
        items = super().get_all()
        self.items = {}
        for i in items:
            self.items[i[self.key_id]] = i

    def add_item(self, data: dict, response: dict) -> int:
        id = response["data"]
        data = {
            self.key_id: id,
            self.key_name: data[self.key_name],
            "debito_Credito": data["debito_Credito"]
        }
        self.items[id] = data
        return id

    def item_id(self, data):
        for key, item in apiCard.items.items():
            if (item["descricao"] == data["descricao"]
                    and item["debito_Credito"] == data["debito_Credito"]):
                return key
        return 0
