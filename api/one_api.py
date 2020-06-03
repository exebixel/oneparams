import json, requests

class one_api():

    def __init__(self, access_token=""):
        self.__api_url = "https://oneapinovo.azurewebsites.net/api"

        if access_token != "":
            self.__header = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
        else:
            self.__header = ""

        self.__gservisId = []
        self.__gservisNome = []

        self.__services = []

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
            "gservsId": self.Gservis(gservs)
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

    def all_Gservis(self):
        print("researching service groups")
        response = requests.get(
            "{0}/OGservsServicos/GservsServicos".format(self.__api_url),
            headers = self.__header
        )

        if response.status_code == 200:
            content = json.loads(response.content)
            for gservs in content["Gservs"]:
                self.__gservisId.append(gservs["GservsId"])
                self.__gservisNome.append(gservs["GservsNome"])
            else:
                print("services groups founds")

        else:
            print("erro researching service groups")
            print(f'Erro code: {response.status_code}')
            print(response.content)
            exit()

    def create_Gservis(self,
                       nome):

        dados = {
            "id": "0",
            "nome": nome
        }

        print("creating service group {0}".format(nome))
        response = requests.post(
            "{0}/Gservs/CreateGServsLight".format(self.__api_url),
            data = json.dumps(dados),
            headers = self.__header
        )

        if response.status_code == 200:
            try:
                content = json.loads(response.content)
            except json.decoder.JSONDecodeError:
                print("Erro in convert JSON")

            print("service group {0} created successful".format(nome))
            self.__gservisId.append(content["data"])
            self.__gservisNome.append(nome)
            return content["data"]
        else:
            print("erro creating service group {0}".format(nome))
            print(f'Erro code: {response.status_code}')
            print(content)
            exit()

    def Gservis(self, 
                nome):
        try:
            index = self.__gservisNome.index(nome)
            gservs_id = self.__gservisId[index]
        except ValueError:
            self.all_Gservis()
            try:
                index = self.__gservisNome.index(nome)
                gservs_id = self.__gservisId[index]
            except ValueError:
                gservs_id = self.create_Gservis(nome)
        finally:
            return gservs_id

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
