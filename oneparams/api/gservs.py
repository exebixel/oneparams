import json

from oneparams.api.base import BaseApi


class Gservis(BaseApi):
    def __init__(self):
        self.__gservis = []
        self.all_Gservis()

    def all_Gservis(self):
        print("researching service groups")
        response = self.get("/OGservsServicos/GservsServicos")
        self.status_ok(response)

        content = json.loads(response.content)
        for gservs in content["Gservs"]:
            self.__gservis.append({
                "id": gservs["GservsId"],
                "nome": gservs["GservsNome"],
                "cont": len(gservs["Servicos"])
            })

    def create_Gservis(self, nome):

        dados = {"nome": nome}

        print("creating service group {0}".format(nome))
        response = self.post("/Gservs/CreateGServsLight", data=dados)
        self.status_ok(response)

        content = json.loads(response.content)
        self.__gservis.append({"id": content["data"], "nome": nome, "cont": 0})
        return content["data"]

    def delete(self, gserv_id):
        for i in range(len(self.__gservis)):
            if self.__gservis[i]["id"] == gserv_id:
                gserv_nome = self.__gservis[i]["nome"]
                break

        print("deleting {} service group".format(gserv_nome))
        response = super().delete("/Gservs/DeleteGservs/{0}".format(gserv_id))
        self.status_ok(response)

        self.__gservis.pop(i)

    def Gservis(self, nome):
        for gserv in self.__gservis:
            if gserv["nome"] == nome:
                return gserv["id"]
        else:
            gservs_id = self.create_Gservis(nome)
            return gservs_id

    def clear(self):
        for gserv in self.__gservis:
            if gserv["cont"] == 0:
                self.delete(gserv["id"])
