import json, requests, sys
from urllib.parse import quote

class login():

    def __init__(self):
        self.__api_url = "https://oneapinovo.azurewebsites.net/api"
        self.__header = {
            'Content-Type': 'application/json',
        }

    def login(self,
              nome_empresa,
              email,
              senha,
              nome_filial = ""):

        empresa = self.empresa(nome_empresa, nome_filial)
        dados = {
            "empresaId": empresa["id"],
            "filialId": empresa["filial_id"],
            "email": email,
            "senha": senha
        }

        print("logging in")
        response = requests.post(
            "{0}/ologin".format(self.__api_url),
            data = json.dumps(dados),
            headers = self.__header
        )

        if response.status_code == 200:
            content = json.loads(response.content)
            access_token =  content["data"]["access_token"]
            print("successful login")
            return access_token

        else:
            print("login erro!")
            print(f'Erro code: {response.status_code}')
            print(response.content)
            sys.exit(0)


    def empresa_id(self, name):

        name = quote(name)
        response = requests.get(
            "{0}/OMobilidades/PesquisarEmpresaPorNome/{1}".format(self.__api_url, name),
            headers = self.__header
        )

        if response.status_code != 200:
            print("Error finding company")
            print(f'Erro code: {response.status_code}')
            print(response.content)
            sys.exit(0)

        content = json.loads(response.content)
        if len(content) != 1:
            print("company not found!!")
            sys.exit(0)

        empresa = {
            "id": content[0]["empresasID"],
            "filial_id": content[0]["filiaisID"],
            "filial": content[0]["temFilial"]
        }
        return empresa


    def filial_id(self, empresa_id, name):

        name = quote(name)
        response = requests.get(
            "{0}/OMobilidades/PesquisarFilialPorNome/{1}/{2}".format(
                self.__api_url,
                empresa_id,
                name
            ),
            headers = self.__header
        )

        if response.status_code != 200:
            print("Error finding branch")
            print(f'Erro code: {response.status_code}')
            print(response.content)
            sys.exit(0)

        content = json.loads(response.content)
        if len(content) != 1:
            print("branch not found!!")
            sys.exit(0)

        return content[0]["filiaisID"]

    def empresa(self, empresa, filial):
        empresa = self.empresa_id(empresa)
        if empresa["filial"]:
            empresa["filial_id"] = self.filial_id(empresa["id"], filial)
        return empresa
