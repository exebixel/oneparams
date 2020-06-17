import json, requests, sys, re
from api.base import base_api
from utils import *

class colaboradores(base_api):

    def __init__(self):
        self.__colaboradores = []
        self.__perfils = []

        self.all_perfils()
        self.all_colaboradores()

    def create(self,
               nome,
               email,
               celular,
               agendavel = True,
               perfil = "colaborador",
               profissao = None):

        dados = {
            "agendavelMobilidade": "true",
            "ativoColaborador": "true",
            "flagCliente": "true",
            "flagFornecedor": "true",
            "agendavel": agendavel,
            "celular": celular,
            "email": email,
            "nomeCompleto": nome,
            "profissaoId": self.profissao_id(profissao),
            "perfilId": self.perfil_id(perfil)
        }

        print("creating {} collaborator".format(nome))
        response = self.post(
            "/OCliForColsUsuarioPerfil/CreateColaboradores",
            data= dados
        )
        self.status_ok(response)

        content = json.loads(response.content)
        self.__colaboradores.append({
            "id": content["data"],
            "nome": nome,
            "email": email,
            "celular": celular,
            "perfil": perfil,
            "profissao": profissao,
            "agendavel": agendavel
        })

    def update(self,
               col_id,
               nome,
               email,
               celular,
               agendavel,
               perfil,
               profissao):

        dados = {
            "flagCliente": "true",
            "flagFornecedor": "true",
            "colaboradorId": col_id,
            "agendavel": agendavel,
            "celular": celular,
            "email": email,
            "nomeCompleto": nome,
            "profissaoId": self.profissao_id(profissao),
            "perfilId": self.perfil_id(perfil)
        }

        print("updating {} collaborator".format(nome))
        response = self.put(
            "/OCliForColsUsuarioPerfil/UpdateColaboradores/{}".format(col_id),
            data = dados
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
                    "nome": i["descricao"]
                })

    def perfil_id(self, nome):
        for perfil in self.__perfils:
            if ( re.search(nome, perfil["nome"], re.IGNORECASE) ):
                return perfil["id"]
        else:
            print("Perfil not found!!")
            sys.exit()

    def profissao_id(self, nome):
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
                    "id": i["cliForColsId"],
                    "nome": i["nomeCompleto"],
                    "email": i["email"],
                    "celular": i["celular"]
                })

    def details(self, nome):
        cont = 0
        for i in self.__colaboradores:
            if i["nome"] == nome:
                cols_id = i["id"]
                break
            cont += 1
        else:
            print("colaborador not found!!")

        response = self.get("/OColaborador/DetalhesColaboradores/{}".format(cols_id))
        self.status_ok(response)

        content = json.loads(response.content)
        col = content["colaboradoresCliForColsLightModel"]
        return {
            "id": cols_id,
            "nome": col["nomeCompleto"],
            "celular": col["celular"],
            "email": col["email"],
            "perfil": content["perfil"],
            "perfilId": col["perfilId"],
            "profissao": content["profissao"],
            "agendavel": col["agendavel"]
        }

    def exist(self, nome):
        for i in self.__colaboradores:
            if i["nome"] == nome:
                return True
        return False

    def equals(self, data):
        col = self.details(data["nome"])
        cont = 0
        for key in data.keys():
            if key == "perfil":
                if col["perfilId"] == self.perfil_id(data[key]):
                    cont += 1
                    continue
            if key == "profissao":
                if self.profissao_id(data[key]) == self.profissao_id(col[key]):
                    cont += 1
                    continue
            if key == "celular":
                if data[key] == get_num(col[key]):
                    cont += 1
                    continue

            if col[key] == data[key]:
                cont+=1
        if cont == len(data):
            return True
        return False

    def colaborador_id(self, nome):
        for i in self.__colaboradores:
            if i["nome"] == nome:
                return i["id"]

    def colaborador(self, data):
        if not self.exist(data["nome"]):
            self.create(
                agendavel= data["agendavel"],
                nome= data["nome"],
                celular= data["celular"],
                email= data["email"],
                perfil= data["perfil"],
                profissao= data["profissao"]
            )

        elif not self.equals(data):
            self.update(
                col_id= self.colaborador_id(data["nome"]),
                agendavel= data["agendavel"],
                nome= data["nome"],
                celular= data["celular"],
                email= data["email"],
                perfil= data["perfil"],
                profissao= data["profissao"]
            )
        else:
            print("skiping {0} collaborator".format(data["nome"]))
