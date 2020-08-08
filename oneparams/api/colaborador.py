import json
import re
import sys

from oneparams.api.base_diff import BaseDiff
from oneparams.api.profissao import Profissao
from oneparams.utils import deemphasize, similar


class Colaboradores(BaseDiff):
    def __init__(self):
        super().__init__(
            key_id="colaboradorId",
            key_name="nomeCompleto",
            item_name="collaborator",
            url_create="/OCliForColsUsuarioPerfil/CreateColaboradores",
            url_update="/OCliForColsFiliais/UpdateColaboradores",
            url_get_all="/CliForCols/ListaDetalhesColaboradores",
            url_get_detail="/OColaborador/DetalhesColaboradores")

        self.__perfils = []
        self.all_perfils()
        self.profissao = Profissao()

    def all_perfils(self):
        print("researching perfils")
        response = self.get("/Perfils/ListaPerfils")
        self.status_ok(response)
        content = json.loads(response.content)

        for i in content:
            if not re.search("cliente", i["descricao"], re.IGNORECASE):
                self.__perfils.append(i)

    def perfil_id(self, nome):
        nome = deemphasize(nome)
        len_similar = []
        for perfil in self.__perfils:
            nome_perfil = deemphasize(perfil["descricao"])
            len_similar.append(similar(nome, nome_perfil))

        max_similar = max(len_similar)
        if (max_similar < 0.55 or len_similar.count(max_similar) == 0):
            print(f'Perfil {nome} not found!!')
            sys.exit()
        if len_similar.count(max_similar) > 1:
            print(f'Perfil {nome} is duplicated!!')
            sys.exit()

        return self.__perfils[len_similar.index(max_similar)]["perfilsId"]

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
        data["profissaoId"] = self.profissao.profissao_id(data["profissao"])
        data.pop("profissao")
        data["perfilId"] = self.perfil_id(data["perfil"])
        data.pop("perfil")
        data["ativoColaborador"] = True

        super().diff_item(data)
