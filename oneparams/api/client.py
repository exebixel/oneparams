import json

from oneparams.api.base_diff import BaseDiff
from oneparams.utils import create_cel, create_email


class Cliente(BaseDiff):
    items = []
    list_details = []
    first_get = False

    def __init__(self):
        self.url_get_all = "/CliForCols/ListaDetalhesClientes"
        self.item_name = "client"

        super().__init__(
            key_id="clienteId",
            key_name="nomeCompleto",
            key_active="ativoCliente",
            item_name=self.item_name,
            url_create="/OCliForColsUsuarioPerfil/CreateClientes",
            url_update="/OCliForColsUsuarioFiliais/UpdateClientes",
            url_get_all=self.url_get_all,
            url_get_detail="/OCliente/Detalhesclientes",
            key_detail="clientesCliForColsLightModel",
            url_delete="/OCliForColsUsuario/DeleteCliente",
            url_inactive="/OCliForColsUsuarioFiliais/UpdateClientes"
        )

        if not Cliente.first_get:
            self.get_all()
            Cliente.first_get = True

    def get_all(self):
        print("researching {}".format(self.item_name))
        Cliente.items = []

        response = self.get(f'{self.url_get_all}/true')
        self.status_ok(response)
        content = json.loads(response.content)

        for i in content:
            Cliente.items.append({
                "clienteId": i["cliForColsId"],
                "nomeCompleto": i["nomeCompleto"],
                "email": i["email"],
                "ativoCliente": True
            })

        response = self.get(f'{self.url_get_all}/false')
        content = json.loads(response.content)

        for i in content:
            Cliente.items.append({
                "clienteId": i["cliForColsId"],
                "nomeCompleto": i["nomeCompleto"],
                "email": i["email"],
                "ativoCliente": False
            })

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
        for i in self.items:
            if (i[self.key_name] == data[self.key_name]
                    or i["email"] == data["email"]):
                return i[self.key_id]
        return 0
