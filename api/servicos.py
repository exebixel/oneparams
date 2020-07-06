import json, requests, sys
from api.gservs import gservis
from api.diff_analize import diff_analize

class servicos(diff_analize):

    def __init__(self):
        self.key_id = "servicosId"
        self.key_name = "descricao"
        self.item_name = "service"

        self.url_create = "/Servicos/CreateServicosLight"
        self.url_update = "/Servicos/UpdateServicosLight"
        self.url_get_all = "/OGservsServicos/ListaDetalhesServicosLight"
        self.url_gel_detail = "/OServicos/DetalhesServicosLight"

        self.items = []
        self.get_all()
        self.Gservs = gservis()

    def delete(self, serv_id):
        cont = 0
        for i in self.items:
            if i["servicosId"] == serv_id:
                nome = i["descricao"]
                break
            cont += 1
        else:
            print("service not found!")
            sys.exit()

        print("deleting {} service".format(nome))
        response = super().delete(
            "/Servicos/DeleteServicos/{0}".format(serv_id)
        )

        return self.status_ok(response, erro_exit=False)

    def inactive(self, serv_id):
        cont = 0
        for i in self.items:
            if i["servicosId"] == serv_id:
                nome = i["descricao"]
                break
            cont += 1
        else:
            print("service not found!")
            sys.exit()

        dados = {
            "ServicosAtivo": "false",
            "ServicosId": serv_id
        }

        print("inactivating {} service".format(nome))
        response = self.patch(
            "/servicos/setservicoativo",
            data = dados
        )

        return self.status_ok(response, erro_exit=False)

    def delete_all(self):
        deleted = []

        for servico in self.items:
            if not self.delete(servico["servicosId"]):
                if self.inactive(servico["servicosId"]):
                    deleted.append(servico)
            else:
                deleted.append(servico)

        for i in deleted:
            self.items.remove(i)

    def get_all(self):
        content = super().get_all()
        for i in content:
            if i["flagAtivo"]:
                self.items.append(i)

    def details(self, nome):
        return super().details(nome)["servicoLightModel"]

    def services(self, data):
        data["gservId"] = self.Gservs.Gservis(data["gserv"])
        data.pop("gserv")
        data["valPercComissao"] = "P"
        super().diff_item(data)
