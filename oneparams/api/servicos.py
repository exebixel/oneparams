from oneparams.api.base_diff import BaseDiff
from oneparams.api.gservs import Gservis


class Servicos(BaseDiff):
    """
    Gerenciamento de serviços,
    cria, atualiza, deleta e inativa serviços
    """
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

    def get_all(self):
        self.items = super().get_all()

    def details(self, item_id):
        return super().details(item_id)["servicoLightModel"]

    def diff_item(self, data):
        data["gservId"] = self.gservs.Gservis(data["gserv"])
        data.pop("gserv")
        data["valPercComissao"] = "P"
        data["valPercCustos"] = "P"
        data["flagAtivo"] = True
        super().diff_item(data)
