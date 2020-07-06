import json, requests, sys
from api.base import base_api

class add_diff(base_api):

    def __init__(self,
                 key_id,
                 key_name,
                 item_name,
                 url_update,
                 url_create,
                 url_get_all,
                 url_get_detail):

        self.__key_id = key_id
        self.__key_name = key_name
        self.__item_name = item_name

        self.__url_update = url_update
        self.__url_create = url_create
        self.__url_get_all = url_get_all
        self.__url_get_detail = url_get_detail

        self.items = []
        self.get_all()

    def create(self, data):
        print("creating {} {}".format(
            data[self.__key_name], self.__item_name)
        )
        response = self.post(
            self.__url_create,
            data = data
        )
        self.status_ok(response)

        content = json.loads(response.content)
        return content["data"]

    def update(self, data):
        print("updating {} {}".format(
            data[self.__key_name], self.__item_name)
        )
        response = self.put(
            "{}/{}".format(self.__url_update, data[self.__key_id]),
            data = data
        )
        self.status_ok(response)

        content = json.loads(response.content)
        return content["data"]

    def get_all(self):
        print("researching {}".format(self.__item_name))
        response = self.get(
            self.__url_get_all
        )
        self.status_ok(response)

        return json.loads(response.content)

    def exists(self, nome):
        for i in self.items:
            if i[self.__key_name] == nome:
                return True
        return False

    def equals(self, data):
        detail = self.details(data[self.__key_name])
        cont = 0
        for key in data.keys():
            if detail[key] == data[key]:
                cont+=1
        if cont == len(data):
            return True
        return False

    def item_id(self, nome):
        for i in self.items:
            if i[self.__key_name] == nome:
                return i[self.__key_id]
        return 0

    def details(self, nome):
        item_id = self.item_id(nome)
        response = self.get(
            "{}/{}".format(self.__url_get_detail, item_id)
        )
        self.status_ok(response)
        return json.loads(response.content)

    def diff_item(self, data):
        if not self.exists(data[self.__key_name]):
            item_id = self.create(data)
            data[self.__key_id] = item_id
            self.items.append(data)

        elif not self.equals(data):
            data[self.__key_id] = self.item_id(
                data[self.__key_name]
            )
            self.update(data)

        else:
            print("skiping {} {}".format(
                data[self.__key_name], self.__item_name)
            )
