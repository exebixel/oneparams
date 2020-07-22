import json
import sys
from urllib.parse import quote

from api.base import BaseApi
from utils import deemphasize, similar


class Profissao(BaseApi):
    def __init__(self):
        self.profissoes = [
            {
                "nome": "Cabeleireiro",
                "id": 0
            },
            {
                "nome": "Manicure/Pedicure",
                "id": 0
            },
            {
                "nome": "Depilador",
                "id": 0
            },
            {
                "nome": "Maquiador",
                "id": 0
            },
            {
                "nome": "Esteticista",
                "id": 0
            },
            {
                "nome": "Administrador",
                "id": 0
            },
            {
                "nome": "Massoterapeuta",
                "id": 0
            },
            {
                "nome": "Barbeiro",
                "id": 0
            },
            {
                "nome": "Recepcionista",
                "id": 0
            },
            {
                "nome": "Estoquista",
                "id": 0
            },
            {
                "nome": "Auxiliar",
                "id": 0
            },
            {
                "nome": "Gerente",
                "id": 0
            },
            {
                "nome": "Copeiro",
                "id": 0
            },
        ]

    def profissao_similar(self, nome):
        nome = deemphasize(nome)
        len_similar = []
        for profissao in self.profissoes:
            pro = deemphasize(profissao["nome"])
            len_similar.append(similar(nome, pro))

        max_similar = max(len_similar)
        if (max_similar < 0.6 or len_similar.count(max_similar) == 0):
            print(f'profession {nome} not found!!')
            sys.exit()
        if len_similar.count(max_similar) > 1:
            print(f'profession {nome} is duplicated!!')
            sys.exit()

        return self.profissoes[len_similar.index(max_similar)]

    def get_id(self, nome):
        if nome is None:
            return None

        nome = quote(nome, safe="")
        response = self.get("/Profissoes/PesquisaProfissoes/{}".format(nome))
        self.status_ok(response)
        content = json.loads(response.content)
        if len(content) != 1:
            print(f'profession {nome} not found!!')
            sys.exit()
        return content[0]["profissoesId"]

    def profissao_id(self, nome):
        if nome is None:
            return None

        profissao = self.profissao_similar(nome)
        if profissao["id"] != 0:
            return profissao["id"]

        index = self.profissoes.index(profissao)
        profissao["id"] = self.get_id(profissao["nome"])
        self.profissoes[index] = profissao
        return profissao["id"]
