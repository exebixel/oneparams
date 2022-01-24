from oneparams.api.base_diff import BaseDiff
from oneparams.api.gservs import Gservis


class ApiServicos(BaseDiff):
    """
    Gerenciamento de serviços,
    cria, atualiza, deleta e inativa serviços
    """
    items = {}
    list_details = {}
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
            key_detail="servicoLightModel",
            url_delete="/Servicos/DeleteServicos",
            url_inactive="/OServicosComis/UpdateServicosLight",
            key_active="flagAtivo",
            submodules={"gservId": Gservis()},
            handle_errors={
                "API.SERVICOS.DELETE.REFERENCE": "Cant delete service..."
            })

        if not ApiServicos.first_get:
            self.get_all()
            ApiServicos.first_get = True

    def get_all(self):
        items = super().get_all()
        ApiServicos.items = {}
        for i in items:
            self.items[i[self.key_id]] = {
                self.key_id: i[self.key_id],
                self.key_name: i[self.key_name],
                self.key_active: i[self.key_active]
            }

    def add_item(self, data: dict, response: dict) -> int:
        item_id = response[self.key_id]
        data = {
            self.key_id: item_id,
            self.key_name: data[self.key_name],
            self.key_active: data[self.key_active]
        }
        ApiServicos.items[item_id] = data
        return item_id
