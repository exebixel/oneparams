from oneparams.api.base_diff import BaseDiff
from oneparams.api.gservs import Gservis


class ApiServicos(BaseDiff):
    """
    Gerenciamento de serviços,
    cria, atualiza, deleta e inativa serviços
    """
    items: dict = {}
    list_details: dict = {}
    first_get: bool = False
    name_list: dict = {}

    def __init__(self):
        super().__init__(
            key_id="servicosId",
            key_name="descricao",
            item_name="service",
            keys_search=["descricao"],
            url_create="/Servicos/CreateServicosLight",
            url_update="/OServicosComis/UpdateServicosLight",
            url_get_all="/OGservsServicos/ListaDetalhesServicosLight",
            url_get_detail="/OServicos/DetalhesServicosLight",
            key_detail="servicoLightModel",
            url_delete="/Servicos/DeleteServicos",
            url_inactive="/OServicosComis/UpdateServicosLight",
            key_active="flagAtivo",
            submodules={"gservId": Gservis()},
            handle_errors={
                "API.SERVICOS.DELETE.REFERENCE":
                "Cant delete '{name}' service..."
            })

        if not ApiServicos.first_get:
            self.get_all()
            ApiServicos.first_get = True

    def get_all(self):
        ApiServicos.items = {}
        ApiServicos.name_list = {}
        return super().get_all()

    def add_item(self, data: dict, response: dict) -> int:
        response["data"] = response[self.key_id]
        return super().add_item(data, response)
