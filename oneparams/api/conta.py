import json
import re

from oneparams.api.base import BaseApi


class conta(BaseApi):
    def __init__(self):
        self.__contas = []
        self.all_contas()

    def all_contas(self):
        print("researching accounts")
        response = self.get("/OContas/ListaContasDetalhes")
        self.status_ok(response)

        content = json.loads(response.content)
        for i in content:
            self.__contas.append(i)

    def get_id(self, nome):
        for i in self.__contas:
            if re.search(nome, i["nome"], re.IGNORECASE):
                return i["contasId"]
        return None
