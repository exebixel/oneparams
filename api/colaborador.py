import json, requests, sys, re
from api.base import base_api
from utils import *

class colaboradores(base_api):

    def __init__(self):
        self.__colaboradores = []
        self.__perfils = []

        self.all_perfils()
        self.all_colaboradores()

    def create(self, data):

        print("creating {} collaborator".format(data["nomeCompleto"]))
        response = self.post(
            "/OCliForColsUsuarioPerfil/CreateColaboradores",
            data= data
        )
        self.status_ok(response)

        content = json.loads(response.content)
        data["colaboradorId"] = content["data"]
        self.__colaboradores.append(data)

    def update(self, data):

        print("updating {} collaborator".format(data["nomeCompleto"]))
        response = self.put(
            "/OCliForColsUsuarioPerfil/UpdateColaboradores/{}".format(
                data["colaboradorId"]
            ),
            data = data
        )
        self.status_ok(response)

    def all_perfils(self):

        print("researching collaborators")
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
        if nome == "":
            return self.perfil_id("colaborador")
        for perfil in self.__perfils:
            if ( re.search(nome, perfil["nomeCompleto"], re.IGNORECASE) ):
                return perfil["id"]
        else:
            print("Perfil not found!!")
            sys.exit()

    def profissao_id(self, nome):
        if nome == "":
            return None

        response = self.get(
            "/Profissoes/PesquisaProfissoes/{}".format(nome)
        )
        self.status_ok(response)
        content = json.loads(response.content)
        if len(content) != 1:
            print("profession not found!!")
            sys.exit()
        return content[0]["profissoesId"]

    def all_colaboradores(self):
        response = self.get("/CliForCols/ListaDetalhesColaboradores")
        self.status_ok(response)

        content = json.loads(response.content)
        for i in content:
            if i["ativoColaborador"]:
                self.__colaboradores.append({
                    "colaboradorId": i["cliForColsId"],
                    "nomeCompleto": i["nomeCompleto"]
                })

    def details(self, nome):
        cont = 0
        for i in self.__colaboradores:
            if i["nomeCompleto"] == nome:
                cols_id = i["colaboradorId"]
                break
            cont += 1
        else:
            print("colaborador not found!!")

        response = self.get(
            "/OColaborador/DetalhesColaboradores/{}".format(cols_id)
        )
        self.status_ok(response)

        content = json.loads(response.content)
        return content["colaboradoresCliForColsLightModel"]

    def exist(self, nome):
        for i in self.__colaboradores:
            if i["nomeCompleto"] == nome:
                return True
        return False

    def equals(self, data):
        col = self.details(data["nomeCompleto"])
        cont = 0
        for key in data.keys():
            if col[key] == data[key]:
                cont+=1

        if cont == len(data):
            return True
        return False

    def colaborador_id(self, nome):
        for i in self.__colaboradores:
            if i["nomeCompleto"] == nome:
                return i["colaboradorId"]

    def colaborador(self, data):
        data["profissaoId"] = self.profissao_id(data["profissao"])
        data.pop("profissao")
        data["perfilId"] = self.perfil_id(data["perfil"])
        data.pop("perfil")
        data["ativoColaborador"] = True

        if not self.exist(data["nomeCompleto"]):
            self.create(data)

        elif not self.equals(data):
            data["colaboradorId"] = self.colaborador_id(
                data["nomeCompleto"]
            )
            self.update(data)

        else:
            print("skiping {0} collaborator".format(data["nomeCompleto"]))
