import json

from oneparams.api.base import BaseApi


class Gservis(BaseApi):
    items = []
    first_get = False

    def __init__(self):
        if not Gservis.first_get:
            self.all_Gservis()
            Gservis.first_get = True

    def all_Gservis(self):
        print("researching service groups")
        response = self.get("/OGservsServicos/GservsServicos")
        self.status_ok(response)

        content = json.loads(response.content)
        Gservis.items = []
        for gservs in content["Gservs"]:
            Gservis.items.append({
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
        Gservis.items.append({"id": content["data"], "nome": nome, "cont": 0})
        return content["data"]

    def delete(self, gserv_id):
        for i in range(len(Gservis.items)):
            if Gservis.items[i]["id"] == gserv_id:
                gserv_nome = Gservis.items[i]["nome"]
                break

        print("deleting {} service group".format(gserv_nome))
        response = super().delete("/Gservs/DeleteGservs/{0}".format(gserv_id))
        self.status_ok(response)

    def return_id(self, nome):
        for gserv in Gservis.items:
            if gserv["nome"] == nome:
                return gserv["id"]
        else:
            gservs_id = self.create_Gservis(nome)
            return gservs_id

    def clear(self):
        deleted = []
        for gserv in Gservis.items:
            if gserv["cont"] == 0:
                self.delete(gserv["id"])
                deleted.append(gserv)
        for i in deleted:
            Gservis.items.remove(i)
