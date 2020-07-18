import json
import re
import sys

from api.base_diff import BaseDiff


class Colaboradores(BaseDiff):
    def __init__(self):
        super().__init__(
            key_id="colaboradorId",
            key_name="nomeCompleto",
            item_name="collaborator",
            url_create="/OCliForColsUsuarioPerfil/CreateColaboradores",
            url_update="/OCliForColsUsuarioPerfil/UpdateColaboradores",
            url_get_all="/CliForCols/ListaDetalhesColaboradores",
            url_get_detail="/OColaborador/DetalhesColaboradores")

        self.__perfils = []
        self.all_perfils()

    def all_perfils(self):
        print("researching perfils")
        response = self.get("/Perfils/ListaPerfils")
        self.status_ok(response)
        content = json.loads(response.content)

        for i in content:
            if not re.search("cliente", i["descricao"], re.IGNORECASE):
                self.__perfils.append({
                    "id": i["perfilsId"],
                    "nomeCompleto": i["descricao"]
                })

    def perfil_id(self, nome):
        for perfil in self.__perfils:
            if (re.search(nome, perfil["nomeCompleto"], re.IGNORECASE)):
                return perfil["id"]
        else:
            print("Perfil not found!!")
            sys.exit()

    def profissao_id(self, nome):
        response = self.get("/Profissoes/PesquisaProfissoes/{}".format(nome))
        self.status_ok(response)
        content = json.loads(response.content)
        if len(content) != 1:
            print("profession not found!!")
            sys.exit()
        return content[0]["profissoesId"]

    def get_all(self):
        content = super().get_all()
        for i in content:
            self.items.append({
                "colaboradorId": i["cliForColsId"],
                "nomeCompleto": i["nomeCompleto"]
            })

    def details(self, item_id):
        return super().details(item_id)["colaboradoresCliForColsLightModel"]

    def colaborador(self, data):
        data["profissaoId"] = self.profissao_id(data["profissao"])
        data.pop("profissao")
        data["perfilId"] = self.perfil_id(data["perfil"])
        data.pop("perfil")
        data["ativoColaborador"] = True

        super().diff_item(data)
