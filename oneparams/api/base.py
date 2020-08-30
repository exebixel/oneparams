import json
import sys

import requests


class BaseApi:
    """
    Classe base da api,
    contem a url base, cuida do access_token
    e do json dumps
    """

    header = {'Content-Type': 'application/json'}

    def __init_subclass__(cls):
        cls.api_url = "https://oneapilite.azurewebsites.net/api"

    def update_token(self, token):
        """
        Atualiza o token de acesso
        """
        BaseApi.header = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }

    def post(self, url, data):
        """
        Post request, url base já inclusa
        """
        return requests.post("{}{}".format(self.api_url, url),
                             headers=self.header,
                             data=json.dumps(data))

    def get(self, url):
        """
        Get request, irl base já inclusa
        """
        return requests.get("{}{}".format(self.api_url, url),
                            headers=self.header)

    def delete(self, url):
        """
        Delete request, url base já inclusa
        """
        return requests.delete("{}{}".format(self.api_url, url),
                               headers=self.header)

    def put(self, url, data):
        """
        Put request, url base já inclusa
        """
        return requests.put("{}{}".format(self.api_url, url),
                            headers=self.header,
                            data=json.dumps(data))

    def patch(self, url, data):
        """
        Patch requests, url base já inclusa
        """
        return requests.patch("{}{}".format(self.api_url, url),
                              headers=self.header,
                              data=json.dumps(data))

    def status_ok(self, response, erro_exit=True):
        """
        verifica se e requisição foi feita com sucesso (200),
        por padrão se a requisição falhou o programa é encerrado,
        é possivel alterar isso com erro_exit=False
        """
        if response.status_code != 200:
            print(f'Erro code: {response.status_code}')
            print(response.content)
            if erro_exit:
                sys.exit()
            return False
        return True
