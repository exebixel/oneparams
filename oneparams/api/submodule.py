import json
from abc import ABC, abstractmethod
from urllib.parse import quote

from oneparams.api.base_diff import BaseDiff


class SubModuleApi(BaseDiff, ABC):

    def __init__(self,
                 key_id: str,
                 key_name: str,
                 item_name: str,
                 url_search: str,
                 url_create: str = None) -> None:

        super().__init__(key_id=key_id,
                         key_name=key_name,
                         item_name=item_name,
                         url_create=url_create)

        self.__url_search = url_search

    @property
    @abstractmethod
    def items(self):
        raise NotImplementedError

    def search(self, name: str) -> list:
        """ Pesquisa por um item

        Argumentos: name: nome a ser pesquisado na api

        Faz uma requisição para a api usando a rota
        definida em self.url_create e adiciona o retorno em
        self.items, alem de retornar os dados em uma lista
        """
        name = quote(name)
        response = self.get(f"{self.__url_search}?{self.key_name}={name}")
        self.status_ok(response)

        content = json.loads(response.content)
        for i in content:
            self.add_item(i, i)
        return content

    def add_item(self, data: dict, response: dict) -> int:
        item_id = response[self.key_id]
        self.items[item_id] = data

    def submodule_id(self, name: str) -> int:
        """ Tenta retornar um id referente ao argamunto passado

        Argumentos: name = nome que sera pesquisado

        Tenta pesqusar nos items já salvos para retornar o id,
        caso não consiga faz uma pesquisa na api,
        caso não encontre nada, tenta criar o item,
        caso não consiga retorna exception com item não encontrado
        """
        item_id = self.item_id(name)
        if item_id != 0:
            return item_id

        # pesquisa na api
        self.search(name)
        item_id = self.item_id(name)
        if item_id != 0:
            return item_id

        # cria o item
        item_id = self.create({self.key_name: name})
        if item_id is not None:
            return item_id

        raise ValueError(f"{self.item_name} {name} not found!")
