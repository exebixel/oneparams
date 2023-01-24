import json
import sys
from urllib3.exceptions import InsecureRequestWarning

import requests


class BaseApi:
    """
    Classe base da api,
    contem a URL base, cuida do access_token
    e do json dumps
    """

    header = {'Content-Type': 'application/json'}
    api_url = "https://oneapilite.azurewebsites.net/api"

    # api_url = "https://oneapilite-preprod.azurewebsites.net/api"
    # api_url = "https://localhost:5001/api"

    def __init_subclass__(cls):
        requests.packages.urllib3.disable_warnings(
            category=InsecureRequestWarning)

    def update_token(self, token: str) -> None:
        """
        Atualiza o token de acesso
        """
        BaseApi.header = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }

    def post(self, url: str, data: dict) -> requests.Response:
        """
        Post request, URL base já inclusa
        """
        try:
            return requests.post(f"{self.api_url}{url}",
                                 headers=self.header,
                                 verify=False,
                                 timeout=20,
                                 data=json.dumps(data))
        except requests.exceptions.ConnectionError:
            sys.exit("\nConnection error!!\nCheck your internet connection")

    def get(self, url: str) -> requests.Response:
        """
        Get request, URL base já inclusa
        """
        try:
            return requests.get(f"{self.api_url}{url}",
                                headers=self.header,
                                timeout=20,
                                verify=False)
        except requests.exceptions.ConnectionError:
            sys.exit("\nConnection error!!\nCheck your internet connection")

    def delete(self, url: str) -> requests.Response:
        """
        Delete request, URL base já inclusa
        """
        try:
            return requests.delete(f"{self.api_url}{url}",
                                   headers=self.header,
                                   timeout=20,
                                   verify=False)
        except requests.exceptions.ConnectionError:
            sys.exit("\nConnection error!!\nCheck your internet connection")

    def put(self, url: str, data: dict) -> requests.Response:
        """
        Put request, URL base já inclusa
        """
        try:
            return requests.put(f"{self.api_url}{url}",
                                headers=self.header,
                                verify=False,
                                timeout=20,
                                data=json.dumps(data))
        except requests.exceptions.ConnectionError:
            sys.exit("\nConnection error!!\nCheck your internet connection")

    def patch(self, url: str, data: dict) -> requests.Response:
        """
        Patch requests, URL base já inclusa
        """
        try:
            return requests.patch(f"{self.api_url}{url}",
                                  headers=self.header,
                                  verify=False,
                                  timeout=20,
                                  data=json.dumps(data))
        except requests.exceptions.ConnectionError:
            sys.exit("\nConnection error!!\nCheck your internet connection")

    def status_ok(self, response: requests.Response) -> bool:
        """
        verifica se e requisição foi feita com sucesso (200),
        por padrão se a requisição falhou o programa é encerrado,
        é possível alterar isso com erro_exit=False
        """
        if not response.ok:
            print(response.text)
            sys.exit(1)
            return False
        return True
