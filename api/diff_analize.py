import json, requests, sys

class diff_analize(base_api):

    def __init__(self):
        self.__key_id = ""
        self.__key_name = ""
        self.__item_name = ""

        self.__url_update = ""
        self.__url_create = ""
        self.__url_delete = ""
        self.__url_inactive = ""
        self.__url_get_all = ""
        self.__url_gel_detail = ""

    def __sub_init__(self):
        self.__items = []
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

    def delete(self, item_id):
        for i in self.__items:
            if i[self.__key_id] == item_id:
                nome = i[self.__item_name]
                break
        else:
            print("{} not found!".format(self.__item_name))
            sys.exit()

        print("deleting {} {}".format(nome, self.__item_name))
        response = super().delete(
            "{}/{}".format(self.__url_delete, item_id)
        )

        return self.status_ok(response, erro_exit=False):


    def get_all(self):
        print("researching {}".format(self.__item_name))
        response = self.get(
            self.__url_get_all
        )
        self.status_ok(response)

        return json.loads(response.content)

    def exists(self, nome):
        for i in self.__items:
            if i[self.__key_id] == nome:
                return True
        return False

    def equals(self, data):
        detail = self.details(data[self.__item_name])
        cont = 0
        for key in data.keys():
            if detail[key] == data[key]:
                cont+=1
        if cont == len(data):
            return True
        return False

    def service_id(self, nome):
        for i in self.__items:
            if i[self.__key_name] == nome:
                return i[self.__key_id]
        return 0

    def details(self, nome):
        serv_id = self.service_id(nome)
        response = self.get(
            "{}{}".format(self.__url_gel_detail, serv_id)
        )
        self.status_ok(response)
        return json.loads(response.content)

    def diff_item(self, data):
        if not self.exists(data[self.__key_name]):
            service_id = self.create(data)

        elif not self.equals(data):
            data[self.__key_id] = self.service_id(data[self.__key_name])
            self.update(data)
        else:
            print("skiping {} {}".format(
                data[self.__key_name], self.__item_name)
            )
