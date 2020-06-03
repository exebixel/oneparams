import json, requests

class login():

    def __init__(self):
        self.__api_url = "https://oneapinovo.azurewebsites.net/api"

    def login(self,
              empresaId: str,
              filialId: str,
              email: str,
              senha: str) -> str:

        header = {
            'Content-Type': 'application/json',
        }
        dados = {
            "empresaId": empresaId,
            "filialId": filialId,
            "email": email,
            "senha": senha
        }

        try:
            print("logging in")
            response = requests.post(
                "{0}/ologin".format(self.__api_url),
                data = json.dumps(dados),
                headers = header
            )

            content = json.loads(response.content)
            access_token =  content["data"]["access_token"]
            print("successful login")
            return access_token

        except:
            print("login erro!")
            print(f'Erro code: {response.status_code}')
            print(response.content)
            exit()
