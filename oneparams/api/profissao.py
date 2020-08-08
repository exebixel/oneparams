import json
import sys

from oneparams.api.base import BaseApi
from oneparams.utils import deemphasize, similar


class Profissao(BaseApi):
    def __init__(self):
        self.profissoes = []
        self.get_all()

    def get_all(self):
        print("researching professions")
        response = self.get("/Profissoes/GetAllProfissoes")
        self.status_ok(response)
        content = json.loads(response.content)
        self.profissoes = content

    def profissao_id(self, nome):
        if nome is None:
            return None

        nome = deemphasize(nome)
        len_similar = []
        for profissao in self.profissoes:
            pro = deemphasize(profissao["descricao"])
            len_similar.append(similar(nome, pro))

        max_similar = max(len_similar)
        if (max_similar < 0.6 or len_similar.count(max_similar) == 0):
            print(f'profession {nome} not found!!')
            sys.exit()
        if len_similar.count(max_similar) > 1:
            print(f'profession {nome} is duplicated!!')
            sys.exit()

        return self.profissoes[len_similar.index(max_similar)]["profissoesId"]
