import json

import pandas as pd
from oneparams.api.base_diff import BaseDiff
from oneparams.api.cidade import ApiCidade
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
            url_create="/OCliForColsUsuarioPerfil/CreateClientesOneParams",
            url_update="/OCliForColsUsuarioFiliais/UpdateClientes",
            url_get_all=self.url_get_all,
            url_get_detail="/OCliente/Detalhesclientes",
            key_detail="clientesCliForColsLightModel",
            url_delete="/OCliForColsUsuario/DeleteCliente",
            url_inactive="/OCliForColsUsuarioFiliais/UpdateClientes",
            submodules={"cidadeId": ApiCidade()})

        if not ApiCliente.first_get:
            self.get_all()
            ApiCliente.first_get = True

    def get_all(self) -> None:
        print(f"researching {self.item_name}")
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

    def equals(self, data: dict) -> None:
        if pd.isnull(data["email"]):
            data.pop("email")
        if pd.isnull(data["celular"]):
            data.pop("celular")
        return super().equals(data)

    def create(self, data: dict) -> None:
        if pd.isnull(data["email"]):
            data["email"] = create_email()
        if pd.isnull(data["celular"]):
            data["celular"] = "00000000"
        super().create(data)

    def update(self, data: dict) -> None:
        if "email" not in data.keys():
            data["email"] = self.details(data[self.key_id])["email"]
        if "celular" not in data.keys():
            data["celular"] = self.details(data[self.key_id])["celular"]
        return super().update(data)

    def item_id(self, data: dict) -> None:
        name = data[self.key_name]
        email = deemphasize(data["email"])

        for key, item in self.items.items():
            existent_name = item[self.key_name]
            existent_email = deemphasize(item["email"]).strip()

            if (existent_name == name or existent_email == email):
                return key
        return 0

    def name_to_id(self, data: dict) -> dict:
        """
        Recebe os dados em um dicionario,
        e transforma os valores dos campos especificados
        no dict self.submodules em ids  \n

        Retorna um novo "data" com os valores
        convertidos para id \n

        Caso ocorra algum erro retorna uma Exception
        """
        if self.submodules is None:
            return data

        if isinstance(data["cidadeId"], int):
            return data

        try:
            city = self.submodules["cidadeId"].submodule_id(
                city=data["cidadeId"], state=data["estadoId"])
            data["estadoId"] = city["estadosId"]
            data["cidadeId"] = city["cidadesId"]
        except ValueError as exp:
            raise ValueError(str(exp)) from exp

        return data
