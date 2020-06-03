import json, requests
from api.gservs import gservis

class servicos():

    def __init__(self, access_token):
        self.__api_url = "https://oneapinovo.azurewebsites.net/api"
        self.__header = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }

        self.__services = []
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
            exit()

    def all_services(self):
        print("researching services")
        response = requests.get(
            "{0}/OGservsServicos/GservsServicos".format(self.__api_url),
            headers = self.__header
        )

        if response.status_code == 200:
            content = json.loads(response.content)
            # if content["Gservs"] == []:
            #     return 0

            cont = 0
            for content in content["Gservs"]:
                for servs in content["Servicos"]:
                    if servs == []:
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
                    return 0

        else:
            print("erro researching service groups")
            print(f'Erro code: {response.status_code}')
            print(response.content)
            exit()

    def services(self,
                 nome,
                 preco,
                 comissao,
                 tempoExecucao,
                 gservs):

        if self.__services != []:
            for services in self.__services:
                if services["nome"] == nome:
                    print("skipping service {0}".format(nome))
                    break

            else:
                service_id = self.create_service(
                    nome = nome,
                    preco = preco,
                    comissao = comissao,
                    tempoExecucao = tempoExecucao,
                    gservs = gservs
                )
                self.__services.append({
                    "id": service_id,
                    "nome": nome,
                    "comissao": comissao,
                    "tempo_execucao": tempoExecucao,
                    "grupo": gservs
                })
        else:
            if self.all_services() != 0:
                self.services(nome,
                              preco,
                              comissao,
                              tempoExecucao,
                              gservs)
            else:
                service_id = self.create_service(
                    nome = nome,
                    preco = preco,
                    comissao = comissao,
                    tempoExecucao = tempoExecucao,
                    gservs = gservs
                )
                self.__services.append({
                    "id": service_id,
                    "nome": nome,
                    "comissao": comissao,
                    "tempo_execucao": tempoExecucao,
                    "grupo": gservs
                })
