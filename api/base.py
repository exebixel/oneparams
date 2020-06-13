import json, requests, sys

class base_api:

    header = {
        'Content-Type': 'application/json'
    }

    def __init_subclass__(self):
        self.api_url = "https://oneapinovo.azurewebsites.net/api"

    def update_token(self, token):
        base_api.header = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }

    def post(self, url, data):
        return requests.post(
            "{}{}".format(self.api_url, url),
            headers = self.header,
            data = json.dumps(data)
        )

    def get(self, url):
        return requests.get(
            "{}{}".format(self.api_url, url),
            headers = self.header
        )

    def delete(self, url):
        return requests.delete(
            "{}{}".format(self.api_url, url),
            headers = self.header
        )

    def put(self, url, data):
        return requests.put(
            "{}{}".format(self.api_url, url),
            headers = self.header,
            data = json.dumps(data)
        )

    def status_ok(self, response, erro_exit=True):
        if response.status_code != 200:
            print(f'Erro code: {response.status_code}')
            print(response.content)
            if erro_exit:
                sys.exit()
            return False
        return True
