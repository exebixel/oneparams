from api.base import base_api
from utils import *
import json

class fornecedor(base_api):

    def __init__(self):
        self.__fornecedores = []
        self.all_fornecedores()

    def all_fornecedores(self):
        print("researching supplier")
        response = self.get("/CliForCols/ListaDetalhesFornecedores")
        self.status_ok(response)

        content = json.loads(response.content)
        for i in content:
            self.__fornecedores.append({
                "id": i["cliForColsId"],
                "nome": i["nomeCompleto"]
            })

    def get_id(self, nome):
        for i in self.__fornecedores:
            if i["nome"] == nome:
                return i["id"]
        return None

    def create(self, nome):
        print("creating {} supplier".format(nome))
        response = self.post(
            "/OCliForColsUsuarioPerfil/CreateFornecedores",
            data = {
                "ativoFornecedor": "true",
                "flagCliente": "false",
                "flagColaborador": "false",
                "email": create_email(),
                "celular": create_cel(),
                "nomeCompleto": nome
            }
        )
        self.status_ok(response)
        content = json.loads(response.content)
        self.__fornecedores.append({
            "id": content["data"],
            "nome": nome
        })
        return content["data"]

    def get_for(self, nome):
        for_id = self.get_id(nome)
        if for_id == None:
            for_id = self.create(nome)
        return for_id
