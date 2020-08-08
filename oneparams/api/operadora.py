import json

from oneparams.api.base import BaseApi
from oneparams.api.fornecedor import Fornecedor


class Operadora(BaseApi):
    def __init__(self):
        self.__operadoras = []
        self.all_operators()
        self.__fornecedor = Fornecedor()

    def all_operators(self):
        print("researching card operators")
        response = self.get("/OperadoraCartoes")
        self.status_ok(response)

        content = json.loads(response.content)
        for content in content:
            self.__operadoras.append({
                "id": content["operadoraCartoesId"],
                "nome": content["descricao"]
            })

    def create(self, nome):
        dados = {
            "descricao": nome,
            "fornecedorId": self.__fornecedor.get_for("Padrão")
        }

        print("creating {} card operator".format(nome))
        response = self.post("/OperadoraCartoes", data=dados)
        self.status_ok(response)

        content = json.loads(response.content)
        self.__operadoras.append({"id": content["data"], "nome": nome})
        return content["data"]

    def delete(self, op_id):
        for i in self.__operadoras:
            if i["id"] == op_id:
                nome = i["nome"]
                break
        else:
            print("card operator not found!!")

        print("deleting {} card operator".format(nome))
        response = super().delete("/OperadoraCartoes/{}".format(op_id))
        self.status_ok(response, erro_exit=False)

    def delete_all(self):
        for i in self.__operadoras:
            self.delete(i["id"])

    def get_id(self, nome):
        for i in self.__operadoras:
            if i["nome"] == nome:
                return i["id"]
        else:
            return None

    def operator(self, nome):
        op_id = self.get_id(nome)
        if op_id is None:
            op_id = self.create(nome)
        return op_id
