import json, requests, sys
from api.gservs import gservis
from api.base import base_api

class servicos(base_api):


    def __init__(self):
        self.__services = []
        self.all_services()
        self.Gservs = gservis()

    def create(self, data):

        # dados = {
        #     "ativo": "true",
        #     "nome": nome,
        #     "preco": preco,
        #     "comissao": comissao,
        #     "tempoExecucao": tempoExecucao,
        #     "gservsId": self.Gservs.Gservis(gservs)
        # }


        print("creating {} service".format(data["descricao"]))
        response = self.post(
            "/Servicos/CreateServicosLight",
            data = data
        )
        self.status_ok(response)

        content = json.loads(response.content)
        return content["data"]

    def update(self, data):

        # dados = {
        #     "descricao": nome,
        #     "preco": preco,
        #     "comissao": comissao,
        #     "tempoExecucao": tempoExecucao,
        #     "gservId": self.Gservs.Gservis(gservs),
        #     "servicosId": service_id
        # }

        print("updating {} service".format(data["descricao"]))
        response = self.put(
            "/Servicos/UpdateServicosLight/{0}".format(data["servicosId"]),
            data = data
        )
        self.status_ok(response)

        content = json.loads(response.content)
        return content["data"]

    def delete(self, serv_id):
        cont = 0
        for i in self.__services:
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

        if self.status_ok(response, erro_exit=False):
            return True
        else:
            return False

    def inactive(self, serv_id):
        cont = 0
        for i in self.__services:
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

        if self.status_ok(response, erro_exit=False):
            return True
        else:
            return False

    def delete_all(self):
        deleted = []

        for servico in self.__services:
            if not self.delete(servico["servicosId"]):
                if self.inactive(servico["servicosId"]):
                    deleted.append(servico)
            else:
                deleted.append(servico)

        for i in deleted:
            self.__services.remove(i)

    def all_services(self):
        print("researching services")
        response = self.get(
            "/OGservsServicos/ListaDetalhesServicosLight"
        )
        self.status_ok(response)

        content = json.loads(response.content)
        for servs in content:
            if servs["flagAtivo"]:
                self.__services.append(servs)

    def exists(self, nome):
        for services in self.__services:
            if services["descricao"] == nome:
                return True
        return False

    def equals(self, data):
        service = self.details(data["descricao"])
        cont = 0
        for key in data.keys():
            if str(service[key]) == data[key]:
                cont+=1
        if cont == len(data):
            return True
        return False

    def service_id(self, nome):
        for services in self.__services:
            if services["descricao"] == nome:
                return services["servicosId"]
        return 0

    def details(self, nome):
        serv_id = self.service_id(nome)
        response = self.get(
            "/OServicos/DetalhesServicosLight/{0}".format(serv_id)
        )
        self.status_ok(response)
        content = json.loads(response.content)
        data = content["servicoLightModel"]
        data["gserv"] = content["grupo"]
        return data

    def services(self, data):
        data["gservId"] = self.Gservs.Gservis(data["gserv"])
        data["valPercComissao"] = "P"
        if not self.exists(data["descricao"]):
            service_id = self.create(data)
            # data["id"] = service_id
            # self.__services.append(data)

        elif not self.equals(data):
            data["servicosId"] = self.service_id(data["descricao"])
            self.update(data)
        else:
            print("skiping {0} service".format(data["descricao"]))
