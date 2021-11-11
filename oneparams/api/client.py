import json

from oneparams.api.base_diff import BaseDiff
from oneparams.utils import create_email, deemphasize


class ApiCliente(BaseDiff):
    items = {}
    list_details = {}
    first_get = False

    def __init__(self):
        self.url_get_all = "/CliForCols/ListaDetalhesClientes"

        super().__init__(
            key_id="clienteId",
            key_name="nomeCompleto",
            key_active="ativoCliente",
            item_name="client",
            url_create="/OCliForColsUsuarioPerfil/CreateClientes",
            url_update="/OCliForColsUsuarioFiliais/UpdateClientes",
            url_get_all=self.url_get_all,
            url_get_detail="/OCliente/Detalhesclientes",
            key_detail="clientesCliForColsLightModel",
            url_delete="/OCliForColsUsuario/DeleteCliente",
            url_inactive="/OCliForColsUsuarioFiliais/UpdateClientes"
        )

        if not ApiCliente.first_get:
            self.get_all()
            ApiCliente.first_get = True

    def get_all(self):
        print("researching {}".format(self.item_name))
        ApiCliente.items = {}

        response = self.get(f'{self.url_get_all}/true')
        self.status_ok(response)
        content = json.loads(response.content)

        for i in content:
            ApiCliente.items[i["cliForColsId"]] = {
                self.key_id: i["cliForColsId"],
                self.key_active: True,
                self.key_name: i[self.key_name],
                "email": i["email"]
            }

        response = self.get(f'{self.url_get_all}/false')
        content = json.loads(response.content)

        for i in content:
            ApiCliente.items[i["cliForColsId"]] = {
                self.key_id: i["cliForColsId"],
                self.key_active: False,
                self.key_name: i[self.key_name],
                "email": i["email"]
            }

    def add_item(self, data: dict, response: dict) -> int:
        data = {
            self.key_active: data[self.key_active],
            self.key_name: data[self.key_name],
            "email": data["email"]
        }
        return super().add_item(data, response)

    def equals(self, data):
        if data["email"] is None:
            data.pop("email")
        if data["celular"] is None:
            data.pop("celular")
        return super().equals(data)

    def create(self, data):
        if data["email"] is None:
            data["email"] = create_email()
        if data["celular"] is None:
            data["celular"] = "00000000"
        super().create(data)

    def update(self, data):
        if "email" not in data.keys():
            data["email"] = self.details(data[self.key_id])["email"]
        if "celular" not in data.keys():
            data["celular"] = self.details(data[self.key_id])["celular"]
        return super().update(data)

    def item_id(self, data):
        name = data[self.key_name]
        email = deemphasize(data["email"])

        for key, item in self.items.items():
            existent_name = item[self.key_name]
            existent_email = deemphasize(item["email"]).strip()

            if (existent_name == name
                    or existent_email == email):
                return key
        return 0
