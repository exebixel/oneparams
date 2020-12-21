import json
import re

from oneparams.api.base import BaseApi


class Conta(BaseApi):
    items = []
    first_get = False

    def __init__(self):
        if not Conta.first_get:
            self.all_contas()
            Conta.first_get = True

    def all_contas(self):
        print("researching accounts")
        response = self.get("/OContas/ListaContasDetalhes")
        self.status_ok(response)

        Conta.items = json.loads(response.content)

    def return_id(self, nome):
        for i in Conta.items:
            if re.search(nome, i["nome"], re.IGNORECASE):
                return i["contasId"]
        return None
