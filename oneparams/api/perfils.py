import json
import re

from oneparams.api.base import BaseApi
from oneparams.utils import deemphasize, similar


class Perfil(BaseApi):
    items = []
    first_get = False

    def __init__(self):
        if not Perfil.first_get:
            self.all_perfils()
            Perfil.first_get = True

    def all_perfils(self):
        print("researching perfils")
        response = self.get("/Perfils/ListaPerfils")
        self.status_ok(response)
        content = json.loads(response.content)

        for i in content:
            if not re.search("cliente", i["descricao"], re.IGNORECASE):
                Perfil.items.append(i)

    def submodule_id(self, nome):
        nome = deemphasize(nome)
        len_similar = []
        for perfil in self.items:
            nome_perfil = deemphasize(perfil["descricao"])
            len_similar.append(similar(nome, nome_perfil))

        max_similar = max(len_similar)
        if (max_similar < 0.55 or len_similar.count(max_similar) == 0):
            raise ValueError(f"Perfil '{nome}' not found!!")
        if len_similar.count(max_similar) > 1:
            raise ValueError(f"Perfil '{nome}' is duplicated!!")

        return Perfil.items[len_similar.index(max_similar)]["perfilsId"]
