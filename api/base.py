import json, requests, sys

class base_api:

    header = {
        'Content-Type': 'application/json'
        # 'Authorization': f'Bearer {access_token}'
    }

    def __init_subclass__(self):
        self.api_url = "https://oneapinovo.azurewebsites.net/api"

    def update_token(self, token):
        base_api.header = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }

