from oneparams.api.base_diff import BaseDiff
from oneparams.api.gservs import Gservis


class Servicos(BaseDiff):
    """
    Gerenciamento de serviços,
    cria, atualiza, deleta e inativa serviços
    """
    items = []
    first_get = False

    def __init__(self):
        super().__init__(
            key_id="servicosId",
            key_name="descricao",
            item_name="service",
            url_create="/Servicos/CreateServicosLight",
            url_update="/OServicosComis/UpdateServicosLight",
            url_get_all="/OGservsServicos/ListaDetalhesServicosLight",
            url_get_detail="/OServicos/DetalhesServicosLight",
            url_delete="/Servicos/DeleteServicos",
            url_inactive="/OServicosComis/UpdateServicosLight",
            key_active="flagAtivo")

        self.gservs = Gservis()
        if not Servicos.first_get:
            self.get_all()
            Servicos.first_get = True

    def get_all(self):
        Servicos.items = super().get_all()

    def details(self, item_id):
        return super().details(item_id)["servicoLightModel"]

    def name_to_id(self, data):
        if "gservId" not in data.keys():
            data["gservId"] = self.gservs.Gservis(data["gserv"])
            data.pop("gserv")
        data["valPercComissao"] = "P"
        data["valPercCustos"] = "P"
        data["flagAtivo"] = True
        return data

    def diff_item(self, data):
        data = self.name_to_id(data)
        super().diff_item(data)
