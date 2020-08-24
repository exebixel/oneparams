import json
import sys
from urllib.parse import quote

from oneparams.api.base import BaseApi


class login(BaseApi):
    def login(self, nome_empresa, email, senha, nome_filial=""):
        empresa = self.empresa(nome_empresa, nome_filial)
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

    def empresa_id(self, name):
        name = quote(name)
        response = self.get(
            "/OMobilidades/PesquisarEmpresaPorNome?nomeEmpresa={}".format(
                name))
        self.status_ok(response)

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
        response = self.get(
            "/OMobilidades/PesquisarFilialPorNome?empresaId={}&nomeEmpresaFilial={}"
            .format(empresa_id, name))
        self.status_ok(response)

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
