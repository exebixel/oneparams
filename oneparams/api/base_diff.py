from abc import ABC, abstractmethod
import json
import re
import sys

from requests import Response

from alive_progress import alive_bar
from oneparams.api.base import BaseApi
from oneparams.config import config_bar
from oneparams.utils import deemphasize


class BaseDiff(BaseApi, ABC):
    """
    Base de suporte para adicionar e atualizar items no sistema
    verificando suas existências e diferenças
    """

    @abstractmethod
    def __init__(self,
                 key_id: str,
                 key_name: str,
                 item_name: str,
                 url_get_all: str = None,
                 url_update: str = None,
                 url_create: str = None,
                 url_get_detail: str = None,
                 key_detail: str = None,
                 url_delete: str = None,
                 key_active: str = None,
                 url_inactive: str = None,
                 submodules: dict = None,
                 handle_errors: dict = None):
        """
        Define todas as urls que serão usadas,
        e também as keys do nome e id
        """

        self.key_id = key_id
        self.key_name = key_name
        self.item_name = item_name

        self.__url_update = url_update
        self.__url_create = url_create
        self.__url_get_all = url_get_all
        self.__url_get_detail = url_get_detail
        self.__key_detail = key_detail

        self.__url_delete = url_delete
        self.__url_inactive = url_inactive
        self.key_active = key_active

        self.submodules = submodules
        self.__handle_error = handle_errors

    @property
    @abstractmethod
    def items(self):
        """ Propriedade que vai guardar todos os items cadastrados no sistema
        """
        raise NotImplementedError("items has not implemented")

    @property
    def list_details(self):
        raise NotImplementedError("list_details has not implemented")

    def create(self, data: dict) -> int:
        """
        Recebe um parâmetro com os dados (dict) que devem
        ser adicionados ao sistema,
        executa a requisição de criação, adiciona na listagem de items
        e por fim retorna o id do item criado
        """
        if self.__url_create is None:
            return None

        print(f"creating {data[self.key_name]} {self.item_name}")
        response = self.post(self.__url_create, data=data)
        self.status_ok(response)

        content = json.loads(response.content)
        item_id = self.add_item(data, content)
        return item_id

    def add_item(self, data: dict, response: dict) -> int:
        """
        Recebe data e response, sendo \n
        data = dict com dados recebidos de forma externa \n
        response = resposta da requisição de self.create() \n

        Depois que adicionar os dados a função deve retornar
        o id do item \n

        Essa função serve basicamente para ser reescrita,
        já que (atualmente) não existe um padrão dentro da api para retorno
        dos dados
        """
        item_id = response["data"]
        data[self.key_id] = item_id
        self.items[item_id] = data
        return item_id

    def update(self, data: dict):
        """
        Atualiza os dados de um item já cadastrado no sistema
        """
        if self.__url_update is None:
            return None

        print(f"updating {data[self.key_name]} {self.item_name}")
        response = self.put(f"{self.__url_update}/{data[self.key_id]}",
                            data=data)
        self.status_ok(response)
        content = json.loads(response.content)

        # Atualiza a lista de items
        self.add_item(data, content)

        # Deleta o item atualizado da lista de detalhes
        # isso aqui apesar de deixar um pouco mais lento
        # evita problemas
        self.list_details.pop(data[self.key_id])

        return True

    def get_all(self) -> dict:
        """
        Retorna todos os items cadastrados no sistema \n

        Essa função deve ser sempre reescrita para
        enviar os dados retornados para a variavel
        self.items,
        infelizmente isso é necessário por não haver um
        padrão de retorno dos dados dentro da api
        """
        if self.__url_get_all is None:
            raise Exception(
                "self.__url_get_all not defined, cannot get items!")

        print(f"researching {self.item_name}")
        response = self.get(self.__url_get_all)
        self.status_ok(response)

        return json.loads(response.content)

    def get_all_details(self, inactive: bool = False) -> None:
        """Puxa da api os detalhamentos de todos os items

        Essa função não retorna nada, apenas preenche a variavel
        self.list_details com os dados dos items, isso é feito
        unicamente com o proposito de otimizar algumas pesquisas

        Os detalhes podem ser acessados através da função
        self.details()

        Argumentos:
        inactive -- Caso seja True puxa dados de items inativos também
        """
        if self.__url_get_detail is None:
            return False

        if inactive:
            all_ids = self.items
        else:
            all_ids = self.items_active()

        config_bar()
        with alive_bar(len(all_ids),
                       title=f"Getting {self.item_name} details") as pbar:
            for item_id in all_ids:
                self.details(item_id)
                pbar()

        return True

    def items_active(self) -> dict:
        """Retorna todos os items ativos"""
        if self.key_active is None:
            return self.items
        return {
            key: item
            for (key, item) in self.items.items() if item[self.key_active]
        }

    def len(self, inactive: bool = True):
        """Retorna a quantidade de items

        Argumentos:
        inactive -- Caso True considera os items inativos na contagem
        """
        if inactive:
            return len(self.items)
        return len(self.items_active())

    def equals(self, data: dict) -> bool:
        """
        verifica se os dados de item são iguais aos dados
        já cadastrados no sistema
        retorna True ou False
        """
        detail = self.details(data[self.key_id])
        cont = 0
        for key in data.keys():
            if detail[key] == data[key]:
                cont += 1
        if cont == len(data):
            return True
        return False

    def item_id(self, data) -> int:
        """
        Pesquisa um item e retorna o id dele,
        nessa pesquisa o nome tem que ser exatamente igual,
        então 'Isso' != 'isso'

        O parâmetro data é um dicionario
        data = [self.key_name: str]
        """
        name = deemphasize(data[self.key_name])
        for key, item in self.items.items():
            item_normalized = deemphasize(item[self.key_name])
            if item_normalized == name:
                return key
        return 0

    def search_item_by_name(self, nome: dict, inactive: bool = False) -> int:
        """
        Pesquisa por um nome (self.key_name) e retorna o Id (self.key_id),
        a pesquisa é feita ignorando o case das letras e os acentos,
        então ISSó == iss

        Por segurança se for passado um nome que esteja em duplicidade
        a função retorna uma exception
        """
        nome = deemphasize(nome)
        name_striped = re.findall(r"[a-z]+", nome)

        if inactive:
            id_to_check = self.items
        else:
            id_to_check = self.items_active()

        for n in name_striped:
            ids = []
            for item_id in id_to_check:
                nome_item = deemphasize(self.items[item_id][self.key_name])
                if re.search(n, nome_item):
                    ids.append(item_id)
            id_to_check = ids

        if len(id_to_check) == 1:
            return id_to_check[0]

        if len(id_to_check) > 0:
            second_ids = []
            for item_id in id_to_check:
                if nome == deemphasize(
                        self.items[item_id][self.key_name]).strip():
                    second_ids.append(item_id)
            if len(second_ids) == 1:
                return second_ids[0]

            raise ValueError(f"{self.item_name} '{nome}' is duplicated!")

        raise ValueError(f"{self.item_name} '{nome}' not found!")

    def details(self, item_id: int) -> dict:
        """
        Retorna um dict com as informações do cadastro completo do item
        """
        try:
            return self.list_details[item_id]
        except KeyError:
            response = self.get(f"{self.__url_get_detail}/{item_id}")
            self.status_ok(response)

            content = json.loads(response.content)
            if self.__key_detail is not None:
                content = content[self.__key_detail]

            self.list_details[content[self.key_id]] = content
            return content

        except AttributeError as exp:
            sys.exit(exp)

    def name_to_id(self, data: dict) -> dict:
        """
        Recebe os dados em um dicionario,
        e transforma os valores dos campos especificados
        no dict self.submodules em ids  \n

        Retorna um novo "data" com os valores
        convertidos para id \n

        Caso ocorra algum erro retorna uma Exception
        """
        if self.submodules is None:
            return data

        erros = []
        for sub, func in self.submodules.items():
            if not isinstance(data[sub], int):
                try:
                    data[sub] = func.submodule_id(data[sub])
                except ValueError as exp:
                    erros.append(str(exp))

        if self.key_active is not None:
            data[self.key_active] = True

        if erros:
            raise ValueError(*erros)
        return data

    def diff_item(self, data: dict) -> None:
        """
        Checa se o item (data) recebido já existe,
        se não existir, checa se o item é igual ao que já esta no sistema,
        se for igual, então o item é pulado,
        se tiver dados diferentes o item sera atualizado
        """
        data[self.key_id] = self.item_id(data)
        try:
            data = self.name_to_id(data)
        except ValueError as exp:
            print("ERROR!! " + str(exp))
            sys.exit(1)

        if data[self.key_id] == 0:
            self.create(data)

        elif not self.equals(data):
            self.update(data)

        else:
            print(f"skiping {data[self.key_name]} {self.item_name}")

    def submodule_id(self, name: str) -> int:
        item_id = self.item_id({self.key_name: name})
        if item_id == 0:
            item_id = self.create({self.key_name: name})
            if item_id is not None:
                return item_id
            raise ValueError(f'{self.item_name} {name} not found!')
        return item_id

    def inactive(self, item_id: int) -> bool:
        """ Inativa um item cadastrado

        Retorna um valor boleano informando se o item
        foi inativado ou não
        """
        if self.__url_inactive is None:
            return False

        data = self.details(item_id)
        if not data[self.key_active]:
            return True

        data[self.key_active] = False

        print(f"inactivating {data[self.key_name]} {self.item_name}")
        response = self.put(f"{self.__url_inactive}/{data[self.key_id]}",
                            data=data)

        if not self.status_ok(response):
            return False

        # atualizo o item na lista
        self.items[data[self.key_id]][self.key_active] = False

        return True

    def delete(self, item_id: int) -> bool:
        """Deleta um item

        Caso não consiga deletar o item
        tentara inativar o item

        Retorna True caso consiga deletar ou
        inativar o item
        """
        if self.__url_delete is None:
            return False

        try:
            item = self.items[item_id]
        except KeyError as exp:
            raise KeyError(f'Id {item_id} not found!') from exp

        print(f"deleting {item[self.key_name]} {self.item_name}")
        response = super().delete(f"{self.__url_delete}/{item_id}")

        if not self.status_ok(response, erro_exit=False):
            return self.inactive(item_id)

        self.items.pop(item_id)
        try:
            self.list_details.pop(item_id)
        except (KeyError, AttributeError, NotImplementedError):
            pass
        return True

    def status_ok(self, response: Response, erro_exit: bool = True) -> bool:
        """
        verifica se e requisição foi feita com sucesso (200),
        por padrão se a requisição falhou o programa é encerrado,
        é possível alterar isso com erro_exit=False
        """
        if not response.ok:
            if self.__handle_error is not None:
                for error_key, message in self.__handle_error.items():
                    if error_key == response.text:
                        print(message)
                        break
                else:
                    print(f"ERROR CODE: {response.status_code}")
                    print(response.text)

            if erro_exit:
                print(f"ERROR CODE: {response.status_code}")
                print(response.text)
                sys.exit(1)
            return False
        return True
