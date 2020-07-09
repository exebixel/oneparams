import json, requests, sys
from api.gservs import gservis
from api.base_diff import base_diff

class servicos(base_diff):

    def __init__(self):
        super().__init__(
            key_id = "servicosId",
            key_name = "descricao",
            item_name = "service",

            url_create = "/Servicos/CreateServicosLight",
            url_update = "/Servicos/UpdateServicosLight",
            url_get_all = "/OGservsServicos/ListaDetalhesServicosLight",
            url_get_detail = "/OServicos/DetalhesServicosLight",

            url_delete= "/Servicos/DeleteServicos",
            url_inactive = "/Servicos/UpdateServicosLight",
            key_active = "flagAtivo"
        )

        self.Gservs = gservis()


    def get_all(self):
        content = super().get_all()
        for i in content:
            self.items.append(i)

    def details(self, nome):
        return super().details(nome)["servicoLightModel"]

    def services(self, data):
        data["gservId"] = self.Gservs.Gservis(data["gserv"])
        data.pop("gserv")
        data["valPercComissao"] = "P"
        data["flagAtivo"] = True
        super().diff_item(data)
