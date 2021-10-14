import sys
import json
import re

from oneparams.api.base import BaseApi
from oneparams.utils import deemphasize


class BaseDiff(BaseApi):
    """
    Base de suporte para adicionar e atualizar items no sistema
    verificando suas existências e diferenças
    """

    def __init__(self,
                 key_id: str,
                 key_name: str,
                 item_name: str,
                 url_get_all: str,
                 url_update: str = None,
                 url_create: str = None,
                 url_get_detail: str = None,
                 key_detail: str = None,
                 url_delete: str = None,
                 key_active: str = None,
                 url_inactive: str = None,
                 submodules: dict = None):
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

        self.__submodules = submodules

    def create(self, data: dict) -> int:
        """
        Recebe um parâmetro com os dados (dict) que devem 
        ser adicionados ao sistema,
        executa a requisição de criação, adiciona na listagem de items 
        e por fim retorna o id do item criado
        """
        if self.__url_create is None: 
            return None

        print("creating {} {}".format(data[self.key_name], self.item_name))
        response = self.post(self.__url_create, data=data)
        self.status_ok(response)

        content = json.loads(response.content)
        id = self.add_item(data, content)
        return id

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
        id = response["data"]
        data[self.key_id] = id
        self.items[id] = data
        return id

    def update(self, data: dict) -> None:
        """
        Atualiza os dados de um item já cadastrado no sistema
        """
        if self.__url_update is None:
            return None

        print("updating {} {}".format(data[self.key_name], self.item_name))
        response = self.put("{}/{}".format(self.__url_update,
                                           data[self.key_id]),
                            data=data)
        self.status_ok(response)
        content = json.loads(response.content)

        # Atualiza a lista de items
        self.add_item(data, content)

        # Deleta o item atualizado da lista de detalhes
        # isso aqui apesar de deixar um pouco mais lento
        # evita problemas
        self.list_details.pop(data[self.key_id])

    def get_all(self) -> dict:
        """
        Retorna todos os items cadastrados no sistema \n

        Essa função deve ser sempre reescrita para 
        enviar os dados retornados para a variavel
        self.items,
        infelizmente isso é necessario por não haver um 
        padrão de retorno dos dados dentro da api
        """
        print("researching {}".format(self.item_name))
        response = self.get(self.__url_get_all)
        self.status_ok(response)

        return json.loads(response.content)

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

    def search_item_by_name(self, nome: dict) -> int:
        """
        Pesquisa por um nome (self.key_name) e retorna o Id (self.key_id),
        a pesquisa é feita ignorando o case das letras e os acentos,
        então ISSó == iss

        Por segurança se for passado um nome que esteja em duplicidade
        a função retorna uma exception
        """
        nome = deemphasize(nome)
        ids = []
        for key, item in self.items.items():
            nome_item = deemphasize(item[self.key_name])
            if re.search(nome, nome_item):
                ids.append(key)

        if len(ids) == 1:
            return ids[0]

        if len(ids) == 0:
            raise ValueError("{} {} not found!".format(self.item_name, nome))
        if len(ids) > 0:
            raise ValueError("{} {} is duplicated!".format(
                self.item_name, nome))

    def details(self, item_id: int) -> dict:
        """
        Retorna um dict com as informações do cadastro completo do item
        """
        try:
            return self.list_details[item_id]
        except KeyError:
            response = self.get("{}/{}".format(self.__url_get_detail, item_id))
            self.status_ok(response)

            content = json.loads(response.content)
            if self.__key_detail is not None:
                content = content[self.__key_detail]

            self.list_details[content[self.key_id]] = content
            return content
        
        except AttributeError as e:
            sys.exit(e)

    def name_to_id(self, data: dict) -> dict:
        """
        Recebe os dados em um dicionario, 
        e transforma os valores dos campos especificados 
        no dict self.submodules em ids  \n

        Retorna um novo "data" com os valores
        convertidos para id \n

        Caso ocorra algum erro retorna uma Exception
        """
        if self.__submodules is None:
            return data

        erros = []
        for sub, func in self.__submodules.items():
            if type(data[sub]) is not int:
                try:
                    data[sub] = func.submodule_id(data[sub])
                except ValueError as e:
                    erros.append(str(e))

        if self.key_active is not None:
            data[self.key_active] = True

        if erros != []:
            raise ValueError(erros)
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
        except ValueError as e:
            sys.exit("ERROR!! " + str(e))

        if data[self.key_id] == 0:
            self.create(data)

        elif not self.equals(data):
            self.update(data)

        else:
            print("skiping {} {}".format(data[self.key_name],
                                         self.item_name))

    def submodule_id(self, name) -> int:
        id = self.item_id({self.key_name: name})
        if id == 0:
            id = self.create({self.key_name: name})
            if id is not None:
                return id
            raise ValueError(f'{self.item_name} {name} not found!')
        return id
            

    def delete(self, data: dict) -> bool:
        """
        Delete um item recebido por parametro (data),
        data tem que ter:
        data = [
            self.key_name: str,
            self.key_id: int
        ]
        """
        if self.__url_delete is None:
            return False

        print("deleting {} {}".format(data[self.key_name], self.item_name))
        response = super().delete("{}/{}".format(self.__url_delete,
                                                 data[self.key_id]))

        return self.status_ok(response, erro_exit=False)

    def inactive(self, data: dict) -> bool:
        """
        Inativa um item que é recebido por 'data'
        'data' deve ter:
        data = [
            self.key_name: str,
            self.key_id: int
        ]

        Retorna um valor boleano informando se o item 
        foi inativado ou não
        """
        if self.__url_inactive is None:
            return False

        data = self.details(data[self.key_id])
        if not data[self.key_active]:
            return True

        data[self.key_active] = False

        print("inactivating {} {}".format(data[self.key_name],
                                          self.item_name))
        response = self.put("{}/{}".format(self.__url_inactive,
                                           data[self.key_id]),
                            data=data)

        if not self.status_ok(response, erro_exit=False):
            return False

        # atualizo o item na lista
        self.items[data[self.key_id]][self.key_active] = False

        return True

    def delete_all(self) -> None:
        """
            Deletar ou inativar (se possivel)
            todos os items em self.items
        """
        deleted = []

        for key, item in self.items.items():
            if self.delete(item):
                deleted.append(key)
            else:
                self.inactive(item)

        for i in deleted:
            self.items.pop(i)
            try:
                self.list_details.pop(i)
            except KeyError:
                pass
            except AttributeError:
                pass
