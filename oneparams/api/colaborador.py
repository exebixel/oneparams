import json

from oneparams.api.base_diff import BaseDiff
from oneparams.api.perfils import Perfil
from oneparams.api.profissao import Profissao


class Colaboradores(BaseDiff):
    items = []
    list_details = []
    first_get = False

    def __init__(self):
        super().__init__(
            key_id="colaboradorId",
            key_name="nomeCompleto",
            item_name="collaborator",
            url_create="/OCliForColsUsuarioPerfil/CreateColaboradores",
            url_update="/OCliForColsFiliais/UpdateColaboradores",
            url_get_all="/CliForCols/ListaDetalhesColaboradores",
            url_get_detail="/OColaborador/DetalhesColaboradores",
            submodules={
                "profissao": Profissao(),
                "perfil": Perfil()
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

    def details(self, item_id):
        return super().details(item_id)["colaboradoresCliForColsLightModel"]

    def item_id(self, data):
        for i in self.items:
            if (i[self.key_name] == data[self.key_name]
                    or i["email"] == data["email"]):
                return i[self.key_id]
        return 0
