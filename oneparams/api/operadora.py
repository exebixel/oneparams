from oneparams.api.base_diff import BaseDiff
from oneparams.api.fornecedor import ApiFornecedor


class Operadora(BaseDiff):
    items = {}
    first_get = False

    def __init__(self):
        super().__init__(key_id="operadoraCartoesId",
                         key_name="descricao",
                         item_name="card operator",
                         url_get_all="/OperadoraCartoes",
                         url_create="/OperadoraCartoes",
                         url_update="/OperadoraCartoes",
                         url_delete="/OperadoraCartoes",
                         submodules={"fornecedorId": ApiFornecedor()},
                         handle_errors={
                             "API.OPERADORACARTOES.DELETE.REFERENCE":
                             "Cant delete card operator..."
                         })
        if not Operadora.first_get:
            self.get_all()
            Operadora.first_get = True

    def get_all(self):
        items = super().get_all()
        Operadora.items = {}
        for i in items:
            Operadora.items[i[self.key_id]] = i

    def add_item(self, data: dict, response: dict) -> int:
        data = {
            self.key_name: data[self.key_name],
        }
        return super().add_item(data, response)

    def create(self, data: dict) -> int:
        if "fornecedorId" not in data:
            data["fornecedorId"] = data[self.key_name]
            data = self.name_to_id(data)
        return super().create(data)
