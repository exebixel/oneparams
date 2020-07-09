import json, requests, sys
from api.base import base_api

class base_diff(base_api):

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

    def equals(self, data):
        detail = self.details(data[self.__key_id])
        cont = 0
        for key in data.keys():
            if detail[key] == data[key]:
                cont+=1
        if cont == len(data):
            return True
        return False

    def item_id(self, data):
        for i in self.items:
            if i[self.__key_name] == data[self.__key_name]:
                return i[self.__key_id]
        return 0

    def details(self, item_id):
        response = self.get(
            "{}/{}".format(self.__url_get_detail, item_id)
        )
        self.status_ok(response)
        return json.loads(response.content)

    def diff_item(self, data):
        data[self.__key_id] = self.item_id(data)

        if data[self.__key_id] == 0:
            item_id = self.create(data)
            data[self.__key_id] = item_id
            self.items.append(data)

        elif not self.equals(data):
            self.update(data)

        else:
            print("skiping {} {}".format(
                data[self.__key_name], self.__item_name)
            )


    def delete(self, data):
        if self.__url_delete == None:
            return False

        print("deleting {} {}".format(
            data[self.__key_name], self.__item_name))
        response = super().delete(
            "{}/{}".format(self.__url_delete, data[self.__key_id])
        )

        return self.status_ok(response, erro_exit=False)

    def inactive(self, data):
        if self.__url_inactive == None:
            return False

        data = self.details(data[self.__key_id])
        data[self.__key_active] = False

        print("inactivating {} {}".format(
            data[self.__key_name], self.__item_name))
        response = self.put(
            "{}/{}".format(self.__url_inactive, data[self.__key_id]),
            data = data
        )

        return self.status_ok(response, erro_exit=False)

    def delete_all(self):
        deleted = []

        for item in self.items:
            if self.delete(item):
                deleted.append(item)
            else:
                self.inactive(item)

        for i in deleted:
            self.items.remove(i)
