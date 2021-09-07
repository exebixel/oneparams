import json

from oneparams.api.base_diff import BaseDiff
from oneparams.api.perfils import Perfil
from oneparams.api.profissao import Profissao
from oneparams.utils import create_cel, create_email


class Colaboradores(BaseDiff):
    items = []
    list_details = []
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

        if not Colaboradores.first_get:
            self.get_all()
            Colaboradores.first_get = True

    def get_all(self):
        content = super().get_all()
        Colaboradores.items = []
        for i in content:
            Colaboradores.items.append({
                "colaboradorId": i["cliForColsId"],
                "nomeCompleto": i["nomeCompleto"],
                "email": i["email"]
            })

    def get_sheduler(self):
        response = self.get("/OProfissional/ProfissionaisAgendaveis")
        self.status_ok(response)
        return json.loads(response.content)

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
