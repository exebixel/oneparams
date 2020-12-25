from oneparams.api.base_diff import BaseDiff
from oneparams.api.gservs import Gservis


class Servicos(BaseDiff):
    """
    Gerenciamento de serviços,
    cria, atualiza, deleta e inativa serviços
    """
    items = []
    list_details = []
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
            key_active="flagAtivo",
            submodules={"gserv": Gservis()})

        if not Servicos.first_get:
            self.get_all()
            Servicos.first_get = True

    def get_all(self):
        Servicos.items = super().get_all()

    def details(self, item_id):
        return super().details(item_id)["servicoLightModel"]

    def name_to_id(self, data):
        data["valPercComissao"] = "P"
        data["valPercCustos"] = "P"
        return super().name_to_id(data)
