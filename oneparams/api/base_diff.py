import json
import re
import sys

from oneparams.api.base import BaseApi
from oneparams.utils import deemphasize


class BaseDiff(BaseApi):
    """
    Base de suporte para adicionar e atualizar items no sistema
    verificando suas existências e diferenças
    """
    def __init__(self,
                 key_id,
                 key_name,
                 item_name,
                 url_update,
                 url_create,
                 url_get_all,
                 url_get_detail,
                 url_delete=None,
                 key_active=None,
                 url_inactive=None):
        """
        Define todas as urls que serão usadas,
        e também as keys do nome e id
        """

        self.__key_id = key_id
        self.__key_name = key_name
        self.__item_name = item_name

        self.__url_update = url_update
        self.__url_create = url_create
        self.__url_get_all = url_get_all
        self.__url_get_detail = url_get_detail

        self.__url_delete = url_delete
        self.__url_inactive = url_inactive
        self.__key_active = key_active

        self.items = []
        self.get_all()

    def create(self, data):
        """
        Adiciona um item ao sistema
        """
        print("creating {} {}".format(data[self.__key_name], self.__item_name))
        response = self.post(self.__url_create, data=data)
        self.status_ok(response)

        content = json.loads(response.content)
        return content

    def update(self, data):
        """
        Atualiza os dados de um item já cadastrado no sistema
        """
        print("updating {} {}".format(data[self.__key_name], self.__item_name))
        response = self.put("{}/{}".format(self.__url_update,
                                           data[self.__key_id]),
                            data=data)
        self.status_ok(response)

        content = json.loads(response.content)
        return content

    def get_all(self):
        """
        Retorna todos os items cadastrados no sistema
        """
        print("researching {}".format(self.__item_name))
        response = self.get(self.__url_get_all)
        self.status_ok(response)

        return json.loads(response.content)

    def equals(self, data):
        """
        verifica se os dados de item são iguais aos dados
        já cadastrados no sistema
        retorna True ou False
        """
        detail = self.details(data[self.__key_id])
        cont = 0
        for key in data.keys():
            if detail[key] == data[key]:
                cont += 1
        if cont == len(data):
            return True
        return False

    def item_id(self, data):
        """
        Pesquisa um item e retorna o id dele,
        nessa pesquisa o nome tem que ser exatamente igual,
        então 'Isso' != 'isso'

        O parâmetro data é um dicionario
        data = [self.__key_name: str]
        """
        for i in self.items:
            if i[self.__key_name] == data[self.__key_name]:
                return i[self.__key_id]
        return 0

    def search_item_by_name(self, nome):
        """
        Pesquisa por um nome (self.__key_name) e retorna o Id (self.__key_id),
        a pesquisa é feita ignorando o case das letras e os acentos,
        então ISSó == iss

        Por segurança se for passado um nome que esteja em duplicidade
        o programa é encerrado
        """
        nome = deemphasize(nome)
        ids = []
        for i in self.items:
            nome_item = deemphasize(i[self.__key_name])
            if re.search(nome, nome_item):
                ids.append(i[self.__key_id])

        if len(ids) == 1:
            return ids[0]

        print("{} {} not found!".format(self.__item_name, nome))
        sys.exit(0)

    def details(self, item_id):
        """
        Retorna um dict com as informações do cadastro completo do item
        """
        response = self.get("{}/{}".format(self.__url_get_detail, item_id))
        self.status_ok(response)
        return json.loads(response.content)

    def diff_item(self, data):
        """
        Checa se o item (data) recebido já existe,
        se não existir, checa se o item é igual ao que já esta no sistema,
        se for igual, então o item é pulado,
        se tiver dados diferentes o item sera atualizado
        """
        data[self.__key_id] = self.item_id(data)

        if data[self.__key_id] == 0:
            item_id = self.create(data)
            data[self.__key_id] = item_id
            self.items.append(data)

        elif not self.equals(data):
            self.update(data)

        else:
            print("skiping {} {}".format(data[self.__key_name],
                                         self.__item_name))

    def delete(self, data):
        """
        Delete um item recebido por parametro (data),
        data tem que ter:
        data = [
            self.__key_name: str,
            self.__key_id: int
        ]
        """
        if self.__url_delete is None:
            return False

        print("deleting {} {}".format(data[self.__key_name], self.__item_name))
        response = super().delete("{}/{}".format(self.__url_delete,
                                                 data[self.__key_id]))

        return self.status_ok(response, erro_exit=False)

    def inactive(self, data):
        """
            Inativa um item que é recebido por 'data'
            'data' deve ter:
            data = [
                self.__key_name: str,
                self.__key_id: int
            ]
        """
        if self.__url_inactive is None:
            return False

        data = self.details(data[self.__key_id])
        data[self.__key_active] = False

        print("inactivating {} {}".format(data[self.__key_name],
                                          self.__item_name))
        response = self.put("{}/{}".format(self.__url_inactive,
                                           data[self.__key_id]),
                            data=data)

        return self.status_ok(response, erro_exit=False)

    def delete_all(self):
        """
            Deletar ou inativar (se possivel)
            todos os items em self.items
        """
        deleted = []

        for item in self.items:
            if self.delete(item):
                deleted.append(item)
            else:
                self.inactive(item)

        for i in deleted:
            self.items.remove(i)
