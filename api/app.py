import json

from api.base import BaseApi


class App(BaseApi):
    def __init__(self):
        pass

    def exist(self, data):
        response = self.get(
            "/OMobilidades/VerificarEmailExistenteNoAplicativo/{}".format(
                data["email"]))
        self.status_ok(response)
        return json.loads(response.content)

    def create(self, data):
        response = self.post(
            "/OUsuariosMobilidades/CadastraUsuarioNoAplicativo/", data)
        self.status_ok(response)
