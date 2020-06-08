import json, requests

class gservis():

    def __init__(self, access_token):
        self.__api_url = "https://oneapinovo.azurewebsites.net/api"
        self.__header = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
            }

        self.__gservis = []

        self.all_Gservis()


    def all_Gservis(self):
        print("researching service groups")
        response = requests.get(
            "{0}/OGservsServicos/GservsServicos".format(self.__api_url),
            headers = self.__header
        )

        if response.status_code == 200:
            content = json.loads(response.content)
            for gservs in content["Gservs"]:
                self.__gservis.append({
                    "id": gservs["GservsId"],
                    "nome": gservs["GservsNome"],
                    "cont": len(gservs["Servicos"])
                })

        else:
            print("erro researching service groups")
            print(f'Erro code: {response.status_code}')
            print(response.content)
            sys.exit()

    def create_Gservis(self,
                       nome):

        dados = {
            "nome": nome
        }

        print("creating service group {0}".format(nome))
        response = requests.post(
            "{0}/Gservs/CreateGServsLight".format(self.__api_url),
            data = json.dumps(dados),
            headers = self.__header
        )

        if response.status_code == 200:
            content = json.loads(response.content)

            print("service group {0} created successful".format(nome))
            self.__gservis.append({
                "id": content["data"],
                "nome": nome,
                "cont": 0
            })
            return content["data"]
        else:
            print("erro creating service group {0}".format(nome))
            print(f'Erro code: {response.status_code}')
            print(response.content)
            sys.exit()

    def Gservis(self,
                nome):
        for gserv in self.__gservis:
            if gserv["nome"] == nome:
                return gserv["id"]
        else:
            gservs_id = self.create_Gservis(nome)
            return gservs_id
