import json, requests, sys
from api.base import base_api

class diff_analize(base_api):

    def __init__(self):
        self.key_id = ""
        self.key_name = ""
        self.item_name = ""

        self.url_update = ""
        self.url_create = ""
        self.url_get_all = ""
        self.url_gel_detail = ""

        self.items = []
        self.get_all()

    def create(self, data):
        print("creating {} {}".format(
            data[self.key_name], self.item_name)
        )
        response = self.post(
            self.url_create,
            data = data
        )
        self.status_ok(response)

        content = json.loads(response.content)
        return content["data"]

    def update(self, data):
        print("updating {} {}".format(
            data[self.key_name], self.item_name)
        )
        response = self.put(
            "{}/{}".format(self.url_update, data[self.key_id]),
            data = data
        )
        self.status_ok(response)

        content = json.loads(response.content)
        return content["data"]

    def get_all(self):
        print("researching {}".format(self.item_name))
        response = self.get(
            self.url_get_all
        )
        self.status_ok(response)

        return json.loads(response.content)

    def exists(self, nome):
        for i in self.items:
            if i[self.key_name] == nome:
                return True
        return False

    def equals(self, data):
        detail = self.details(data[self.key_name])
        cont = 0
        for key in data.keys():
            if detail[key] == data[key]:
                cont+=1
        if cont == len(data):
            return True
        return False

    def item_id(self, nome):
        for i in self.items:
            if i[self.key_name] == nome:
                return i[self.key_id]
        return 0

    def details(self, nome):
        item_id = self.item_id(nome)
        response = self.get(
            "{}/{}".format(self.url_gel_detail, item_id)
        )
        self.status_ok(response)
        return json.loads(response.content)

    def diff_item(self, data):
        if not self.exists(data[self.key_name]):
            item_id = self.create(data)
            data[self.key_id] = item_id
            self.items.append(data)

        elif not self.equals(data):
            data[self.key_id] = self.item_id(
                data[self.key_name]
            )
            self.update(data)

        else:
            print("skiping {} {}".format(
                data[self.key_name], self.item_name)
            )
