import json
import sys

import requests


class BaseApi:
    """
    Classe base da api,
    contem a URL base, cuida do access_token
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
        Post request, URL base já inclusa
        """
        try:
            return requests.post("{}{}".format(self.api_url, url),
                                 headers=self.header,
                                 data=json.dumps(data))
        except requests.exceptions.ConnectionError:
            sys.exit("Connection error!!\nCheck your internet connection")

    def get(self, url):
        """
        Get request, URL base já inclusa
        """
        try:
            return requests.get("{}{}".format(self.api_url, url),
                                headers=self.header)
        except requests.exceptions.ConnectionError:
            sys.exit("Connection error!!\nCheck your internet connection")

    def delete(self, url):
        """
        Delete request, URL base já inclusa
        """
        try:
            return requests.delete("{}{}".format(self.api_url, url),
                                   headers=self.header)
        except requests.exceptions.ConnectionError:
            sys.exit("Connection error!!\nCheck your internet connection")

    def put(self, url, data):
        """
        Put request, URL base já inclusa
        """
        try:
            return requests.put("{}{}".format(self.api_url, url),
                                headers=self.header,
                                data=json.dumps(data))
        except requests.exceptions.ConnectionError:
            sys.exit("Connection error!!\nCheck your internet connection")

    def patch(self, url, data):
        """
        Patch requests, URL base já inclusa
        """
        try:
            return requests.patch("{}{}".format(self.api_url, url),
                                  headers=self.header,
                                  data=json.dumps(data))
        except requests.exceptions.ConnectionError:
            sys.exit("Connection error!!\nCheck your internet connection")

    def status_ok(self, response, erro_exit=True):
        """
        verifica se e requisição foi feita com sucesso (200),
        por padrão se a requisição falhou o programa é encerrado,
        é possível alterar isso com erro_exit=False
        """
        if response.status_code != 200:
            print(f'Erro code: {response.status_code}')
            print(response.content)
            if erro_exit:
                sys.exit()
            return False
        return True
