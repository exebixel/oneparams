import json

from oneparams.api.base import BaseApi
from oneparams.utils import deemphasize, similar


class Profissao(BaseApi):
    items = []
    first_get = False

    def __init__(self):
        if not Profissao.first_get:
            self.get_all()
            Profissao.first_get = True

    def get_all(self):
        print("researching professions")
        response = self.get("/Profissoes/GetAllProfissoes")
        self.status_ok(response)
        content = json.loads(response.content)
        Profissao.items = content

    def return_id(self, nome):
        if nome is None:
            return None

        nome = deemphasize(nome)
        len_similar = []
        for profissao in Profissao.items:
            pro = deemphasize(profissao["descricao"])
            len_similar.append(similar(nome, pro))

        max_similar = max(len_similar)
        if (max_similar < 0.6 or len_similar.count(max_similar) == 0):
            raise ValueError(f'profession {nome} not found!!')
        if len_similar.count(max_similar) > 1:
            raise ValueError(f'profession {nome} is duplicated!!')

        return Profissao.items[len_similar.index(max_similar)]["profissoesId"]
