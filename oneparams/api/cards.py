from oneparams.api.base_diff import BaseDiff
from oneparams.api.conta import ApiConta
from oneparams.api.operadora import Operadora
from oneparams.utils import deemphasize


class ApiCard(BaseDiff):
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
                             "contasId": ApiConta(),
                             "operadoraCartaoId": Operadora()
                         },
                         handle_errors={
                             "API.CARTOES.DELETE.REFERENCE": "Cant delete card..."
                         }
        )

        if not ApiCard.first_get:
            self.get_all()
            ApiCard.first_get = True

    def get_all(self):
        items = super().get_all()
        ApiCard.items = {}
        for i in items:
            ApiCard.items[i[self.key_id]] = i

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
        name = deemphasize(data[self.key_name])
        for key, item in self.items.items():
            item_normalized = deemphasize(item[self.key_name])
            if (item_normalized == name 
                    and item["debito_Credito"] == data["debito_Credito"]):
                return key
        return 0