import json, requests, sys
from api.gservs import gservis

class servicos():

    def __init__(self, access_token):
        self.__api_url = "https://oneapinovo.azurewebsites.net/api"
        self.__header = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }

        self.__services = []
        self.all_services()
        self.Gservs = gservis(access_token)

    def create_service(self,
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

        response = requests.post(
            "{0}/Servicos/ServicosBasic".format(self.__api_url),
            data = json.dumps(dados),
            headers = self.__header
        )

        if response.status_code == 200:
            content = json.loads(response.content)
            print("service {0} created successful".format(nome))
            return content["data"]
        else:
            print("erro creating service {0}".format(nome))
            print(f'Erro code: {response.status_code}')
            print(response.content)
            sys.exit()

    def all_services(self):
        print("researching services")
        response = requests.get(
            "{0}/OGservsServicos/GservsServicos".format(self.__api_url),
            headers = self.__header
        )

        if response.status_code == 200:
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
                            "comissao": servs["ServicoValorComissao"],
                            "tempo_execucao": servs["ServicoTempoExecucao"],
                            "grupo": content["GservsNome"]
                        })
            else:
                if cont == 0:
                    return None

        else:
            print("erro researching service groups")
            print(f'Erro code: {response.status_code}')
            print(response.content)
            sys.exit()

    def exists(self, nome):
        for services in self.__services:
            if services["nome"] is nome:
                return True

        return False

    def equals(self, data):
        for services in self.__services:
            services.pop("id")
            if services is data:
                return True

        return False

    def services(self, data):

        if not self.exists(data["nome"]):
            service_id = self.create_service(
                nome = data["nome"],
                preco = data["preco"],
                comissao = data["comissao"],
                tempoExecucao = data["tempo_execucao"],
                gservs = data["grupo"]
            )
            data["id"] = service_id
            self.__services.append(data)

        else:
            print(f'Service {data["nome"]} exist')

        # elif not equals(data):
