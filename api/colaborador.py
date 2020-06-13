import json, requests, sys
from api.base import base_api

class colaborador(base_api):

    def __init__(self):
        self.__colaboradores = []

    def create(self,
               nome,
               email,
               celular,
               agendavel = True,
               perfil = "colaborador",
               profissao = None):

        dados = {

        }
        response = requests.post(
            "{0}/OCliForColsUsuarioPerfil/CreateColaboradores".format(self.__api_url),
            data= json.dumps(dados),
            headers= self.__header
        )

        if response.status_code == 200:
            content = json.loads(response.content)
            self.__colaboradores.append({
                "id": content["data"],
                "nome": nome,
                "email": email,
                "celular": celular,
                "perfil": perfil,
                "profissao": profissao
            })
        else:
            print("error creating {0}collaborator".format(nome))
            print(f'Erro code: {response.status_code}')
            print(response.content)
            sys.exit()

