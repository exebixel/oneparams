import json

from oneparams.api.base import BaseApi
from oneparams.api.fornecedor import Fornecedor


class Operadora(BaseApi):
    items = []
    first_get = False

    def __init__(self):
        if not Operadora.first_get:
            self.all_operators()
            Operadora.first_get = True
        self.__fornecedor = Fornecedor()

    def all_operators(self):
        print("researching card operators")
        response = self.get("/OperadoraCartoes")
        self.status_ok(response)

        content = json.loads(response.content)
        Operadora.items = []
        for content in content:
            Operadora.items.append({
                "id": content["operadoraCartoesId"],
                "nome": content["descricao"]
            })

    def create(self, nome):
        dados = {
            "descricao": nome,
            "fornecedorId": self.__fornecedor.get_for(nome)
        }

        print("creating {} card operator".format(nome))
        response = self.post("/OperadoraCartoes", data=dados)
        self.status_ok(response)

        content = json.loads(response.content)
        Operadora.items.append({"id": content["data"], "nome": nome})
        return content["data"]

    def delete(self, op_id):
        for i in Operadora.items:
            if i["id"] == op_id:
                nome = i["nome"]
                break
        else:
            print("card operator not found!!")

        print("deleting {} card operator".format(nome))
        response = super().delete("/OperadoraCartoes/{}".format(op_id))
        self.status_ok(response, erro_exit=False)

    def delete_all(self):
        deleted = []
        for i in Operadora.items:
            self.delete(i["id"])
            deleted.append(i)
        for i in deleted:
            Operadora.items.remove(i)

    def get_id(self, nome):
        for i in Operadora.items:
            if i["nome"] == nome:
                return i["id"]
        else:
            return None

    def return_id(self, nome):
        op_id = self.get_id(nome)
        if op_id is None:
            op_id = self.create(nome)
        return op_id
