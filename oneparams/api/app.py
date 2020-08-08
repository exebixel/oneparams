import json

from oneparams.api.base import BaseApi


class App(BaseApi):
    def __init__(self):
        pass

    def exist(self, email):
        response = self.get(
            "/OMobilidades/VerificarEmailExistenteNoAplicativo/{}".format(
                email))
        self.status_ok(response)
        return json.loads(response.content)

    def create(self, email, nome, celular):
        print("registering {} in the app".format(nome))
        data = {"nome": nome, "email": email, "celular": celular}
        response = self.post(
            "/OUsuariosMobilidades/CadastraUsuarioNoAplicativo/0", data)
        self.status_ok(response)

    def app(self, email, nome, celular):
        if not self.exist(email):
            self.create(email=email, nome=nome, celular=celular)
        else:
            print("{} user already registered in the app".format(nome))
