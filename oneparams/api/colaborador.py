from oneparams.api.base_diff import BaseDiff
from oneparams.api.perfils import Perfil
from oneparams.api.profissao import Profissao
from oneparams.utils import create_email, deemphasize


class ApiColaboradores(BaseDiff):
    items = {}
    list_details = {}
    first_get = False

    def __init__(self):
        super().__init__(
            key_id="colaboradorId",
            key_name="nomeCompleto",
            key_active="ativoColaborador",
            item_name="collaborator",
            url_create="/OCliForColsUsuarioPerfil/CreateColaboradores",
            url_update="/OCliForColsFiliais/UpdateColaboradores",
            url_get_all="/CliForCols/ListaDetalhesColaboradores",
            url_get_detail="/OColaborador/DetalhesColaboradores",
            key_detail="colaboradoresCliForColsLightModel",
            submodules={
                "profissaoId": Profissao(),
                "perfilId": Perfil()
            })

        if not ApiColaboradores.first_get:
            self.get_all()
            ApiColaboradores.first_get = True

    def get_all(self):
        content = super().get_all()
        ApiColaboradores.items = {}
        for i in content:
            ApiColaboradores.items[i["cliForColsId"]] = {
                self.key_id: i["cliForColsId"],
                self.key_active: i[self.key_active],
                self.key_name: i[self.key_name],
                "email": i["email"],
                "celular": i["celular"]
            }

    def add_item(self, data: dict, response: dict) -> int:
        item_id = response["data"][self.key_id]
        data = {
            self.key_id: item_id,
            self.key_active: data[self.key_active],
            self.key_name: data[self.key_name],
            "email": data["email"],
            "celular": data["celular"]
        }
        self.items[item_id] = data
        return item_id

    def equals(self, data: dict) -> bool:
        if data["email"] is None:
            data.pop("email")
        if data["celular"] is None:
            data.pop("celular")
        return super().equals(data)

    def create(self, data: dict) -> int:
        if data["email"] is None:
            data["email"] = create_email()
        if data["celular"] is None:
            data["celular"] = "00000000"
        super().create(data)

    def update(self, data: dict):
        if "email" not in data.keys():
            data["email"] = self.details(data[self.key_id])["email"]
        if "celular" not in data.keys():
            data["celular"] = self.details(data[self.key_id])["celular"]
        return super().update(data)

    def item_id(self, data: dict) -> int:
        name = deemphasize(data[self.key_name])
        email = deemphasize(data["email"])

        for key, item in self.items.items():
            existent_name = deemphasize(item[self.key_name])
            existent_email = deemphasize(item["email"]).strip()

            if (existent_name == name
                    or existent_email == email):
                return key
        return 0
