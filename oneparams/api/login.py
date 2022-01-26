import json
import sys
from urllib.parse import quote

from oneparams.api.base import BaseApi


class Login(BaseApi):

    def login(self,
              nome_empresa: str,
              email: str,
              senha: str,
              nome_filial: str = None,
              empresa_id: bool = 0) -> bool:
        empresa = self.empresa(nome_empresa, nome_filial, empresa_id)
        dados = {
            "empresaId": empresa["id"],
            "filialId": empresa["filial_id"],
            "email": email,
            "senha": senha
        }

        print("logging in")
        response = self.post("/ologin?empresaId={}&filialId={}".format(
            dados["empresaId"], dados["filialId"]),
                             data=dados)

        if self.status_ok(response):
            content = json.loads(response.content)
            access_token = content["data"]["access_token"]
            print("successful login")
            super().update_token(access_token)

    def empresa_id(self, name: str, empresa_id: bool = 0) -> dict:
        name = quote(name)
        response = self.get(
            f"/OMobilidades/PesquisarEmpresaPorNome?nomeEmpresa={name}")
        self.status_ok(response)

        content = json.loads(response.content)
        if len(content) == 0:
            sys.exit(f'ERROR! Company {name} not found')

        if len(content) > 1:
            content = self.empresa_menu(content, empresa_id)
        if len(content) == 1:
            content = content[0]

        return {
            "id": content["empresasID"],
            "filial_id": content["filiaisID"],
            "filial": content["temFilial"]
        }

    def empresa_menu(self, data: dict, empresa_id: int) -> dict:
        if empresa_id != 0:
            for i in data:
                if i["empresasID"] == empresa_id:
                    return i
            sys.exit("ERROR! Company Id not found in search")

        else:
            print("You need select the company you want to login")
            cont = 0
            for i in data:
                print(f'{cont} - {i["nomeEmpresa"]} - id: {i["empresasID"]}')
                cont += 1
            while True:
                try:
                    choice = int(input("Choose the company: "))
                    if 0 <= choice < cont:
                        break
                    print("Choose a valid company!!")
                except ValueError:
                    print("Choose a valid company!!")

            return data[choice]

    def filial_id(self, empresa_id: int, name: str) -> int:
        name = quote(name)
        response = self.get(
            "/OMobilidades/PesquisarFilialPorNome?empresaId={}&nomeEmpresaFilial={}"
            .format(empresa_id, name))
        self.status_ok(response)

        content = json.loads(response.content)
        if len(content) != 1:
            print("ERROR! Branch not found!!")
            sys.exit(1)

        return content[0]["filiaisID"]

    def empresa(self, empresa: str, filial: str, empresa_id: int = 0) -> dict:
        empresa: dict = self.empresa_id(empresa, empresa_id)
        if empresa["filial"]:
            if filial is None:
                sys.exit(
                    "ERROR! Missing Branch! specify a branch and try again ")
            empresa["filial_id"] = self.filial_id(empresa["id"], filial)
        return empresa
