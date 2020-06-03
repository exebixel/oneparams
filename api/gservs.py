import json, requests

class gservis():

    def __init__(self, access_token):
        self.__api_url = "https://oneapinovo.azurewebsites.net/api"
        self.__header = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
            }

        self.__gservisId = []
        self.__gservisNome = []


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
