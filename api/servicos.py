import json, requests, sys
from api.gservs import gservis
from api.base import base_api

class servicos(base_api):


    def __init__(self):
        self.__services = []
        self.all_services()
        self.Gservs = gservis()

    def create(self,
                       nome,
                       preco,
                       comissao,
                       tempoExecucao,
                       gservs):

        dados = {
            "ativo": "true",
            "nome": nome,
            "preco": preco,
            "comissao": comissao,
            "tempoExecucao": tempoExecucao,
            "gservsId": self.Gservs.Gservis(gservs)
        }

        print("creating {} service".format(nome))
        response = self.post(
            "/Servicos/ServicosBasic",
            data = dados
        )
        self.status_ok(response)

        content = json.loads(response.content)
        return content["data"]

    def update(self,
              service_id,
              nome,
              preco,
              comissao,
              tempoExecucao,
              gservs):

        dados = {
            "descricao": nome,
            "preco": preco,
            "comissao": comissao,
            "tempoExecucao": tempoExecucao,
            "gservId": self.Gservs.Gservis(gservs),
            "servicosId": service_id
        }

        response = self.put(
            "/Servicos/UpdateServicosLight/{0}".format(service_id),
            data = dados
        )
        self.status_ok(response)

        content = json.loads(response.content)
        print("service {0} updated successful".format(nome))
        return content["data"]

    def delete(self, serv_id):
        cont = 0
        for i in self.__services:
            if i["id"] == serv_id:
                nome = i["nome"]
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
            if i["id"] == serv_id:
                nome = i["nome"]
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
            if not self.delete(servico["id"]):
                if self.inactive(servico["id"]):
                    deleted.append(servico)
            else:
                deleted.append(servico)

        for i in deleted:
            self.__services.remove(i)

    def all_services(self):
        print("researching services")
        response = self.get(
            "/OGservsServicos/GservsServicos",
        )
        self.status_ok(response)

        content = json.loads(response.content)

        cont = 0
        for content in content["Gservs"]:
            for servs in content["Servicos"]:
                if servs is not []:
                    cont+=1
                if servs["ServicosAtivo"]:
                    self.__services.append({
                        "id": servs["ServicosId"],
                        "nome": servs["ServicosNome"],
                        "preco": servs["ServicoPreco"],
                        "comissao": servs["ServicoValorComissao"],
                        "tempo_execucao": servs["ServicoTempoExecucao"],
                        "grupo": content["GservsNome"]
                    })
        else:
            if cont == 0:
                return None

    def exists(self, nome):
        for services in self.__services:
            if services["nome"] == nome:
                return True
        return False

    def equals(self, data):
        for services in self.__services:
            cont = 0
            for key in data.keys():
                # services.pop("id")
                if services[key] == data[key]:
                    cont+=1
            if cont == len(data):
                return True
        return False

    def service_id(self, nome):
        for services in self.__services:
            if services["nome"] == nome:
                return services["id"]
        return 0


    def services(self, data):
        if not self.exists(data["nome"]):
            service_id = self.create(
                nome = data["nome"],
                preco = data["preco"],
                comissao = data["comissao"],
                tempoExecucao = data["tempo_execucao"],
                gservs = data["grupo"]
            )
            data["id"] = service_id
            self.__services.append(data)

        elif not self.equals(data):
            self.update(
                service_id = self.service_id(data["nome"]),
                nome = data["nome"],
                comissao = data["comissao"],
                preco = data["preco"],
                tempoExecucao = data["tempo_execucao"],
                gservs = data["grupo"]
            )
        else:
            print("skiping {0} service".format(data["nome"]))
