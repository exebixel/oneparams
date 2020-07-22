import json
import re
import sys

from api.base_diff import BaseDiff
from utils import similar


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

        self.profissoes = [
            "Cabeleireiro",
            "Manicure/Pedicure",
            "Depilador",
            "Maquiador",
            "Esteticista",
            "Administrador",
            "Massoterapeuta",
            "Barbeiro",
            "Recepcionista",
            "Estoquista",
            "Auxiliar",
            "Gerente",
            "Copeiro",
        ]

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
        len_similar = []
        for perfil in self.__perfils:
            len_similar.append(similar(nome, perfil["nomeCompleto"]))

        max_similar = max(len_similar)
        if (max_similar == 0 or len_similar.count(max_similar) == 0):
            print(f'Perfil {nome} not found!!')
            sys.exit()
        if len_similar.count(max_similar) > 1:
            print(f'Perfil {nome} is duplicated!!')
            sys.exit()

        return self.__perfils[len_similar.index(max_similar)]["id"]

    def profissao_id(self, nome):
        if nome is None:
            return None

        len_similar = []
        for profissao in self.profissoes:
            len_similar.append(similar(nome, profissao))

        max_similar = max(len_similar)
        if (max_similar == 0 or len_similar.count(max_similar) == 0):
            print(f'Profissao {nome} not found!!')
            sys.exit()
        if len_similar.count(max_similar) > 1:
            print(f'Profissao {nome} is duplicated!!')
            sys.exit()

        return self.__perfils[len_similar.index(max_similar)]["id"]

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
