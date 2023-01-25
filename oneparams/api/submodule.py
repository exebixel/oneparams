import json
from abc import ABC, abstractmethod
from urllib.parse import quote

from oneparams.utils import deemphasize
from oneparams.api.base_diff import BaseDiff


class SubModuleApi(BaseDiff, ABC):

    def __init__(self,
                 key_id: str,
                 key_name: str,
                 item_name: str,
                 url_search: str,
                 keys_search: list,
                 key_search_term: str = "searchTerm",
                 url_create: str = None,
                 url_delete: str = None) -> None:

        super().__init__(key_id=key_id,
                         key_name=key_name,
                         item_name=item_name,
                         keys_search=keys_search,
                         url_create=url_create,
                         url_delete=url_delete)

        self.__url_search = url_search
        self.__key_search_term = key_search_term

    @property
    @abstractmethod
    def items(self) -> dict:
        raise NotImplementedError

    def search(self, name: str) -> list:
        """ Pesquisa por um item

        Argumentos: name: nome a ser pesquisado na api

        Faz uma requisição para a api usando a rota
        definida em self.url_create e adiciona o retorno em
        self.items, além de retornar os dados em uma lista
        """
        name = quote(name)
        response = self.get(
            f"{self.__url_search}?{self.__key_search_term}={name}")
        if not self.status_ok(response):
            response.raise_for_status()

        content = json.loads(response.content)
        for i in content:
            self.items[i[self.key_id]] = i
            for key in self.keys_search:
                if key not in self.name_list:
                    self.name_list[key] = {}

                value = deemphasize(i[key])
                if value in self.name_list[key]:
                    self.name_list[key][value].append(i[self.key_id])
                else:
                    self.name_list[key][value] = [i[self.key_id]]

        return content

    def submodule_id(self, name: str) -> int:
        """ Tenta retornar um id referente ao argamunto passado

        Argumentos: name = nome que sera pesquisado

        Tenta pesquisar nos items já salvos para retornar o id,
        caso não consiga faz uma pesquisa na api,
        caso não encontre nada, tenta criar o item,
        caso não consiga retorna exception com item não encontrado
        """
        item_id = self.item_id({self.key_name: name})
        if item_id != 0:
            return item_id

        # pesquisa na api
        self.search(name)
        item_id = self.item_id({self.key_name: name})
        if item_id != 0:
            return item_id

        # cria o item
        item_id = self.create({self.key_name: name})
        if item_id is not None:
            return item_id

        raise ValueError(f"{self.item_name} {name} not found!")
