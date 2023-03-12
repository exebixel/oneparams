import json

from oneparams.api.base_diff import BaseDiff


class Gservis(BaseDiff):
    items: dict = {}
    first_get: bool = False
    name_list: dict = {}

    def __init__(self):
        super().__init__(key_id="id",
                         key_name="nome",
                         item_name="service group",
                         keys_search=["nome"],
                         url_get_all="/Gservs/PesquisarGservs",
                         url_create="/Gservs/CreateGServsLight",
                         url_delete="/Gservs/DeleteGservs")

        if not Gservis.first_get:
            self.get_all()
            Gservis.first_get = True

    def get_all(self) -> dict:
        Gservis.items = {}
        Gservis.name_list = {}
        return super().get_all()

    def add_item(self, data: dict, response: dict) -> int:
        data["cont"] = 0
        return super().add_item(data, response)

    def clear(self):
        response = self.get("/OGservsServicos/GservsServicos")
        if not self.status_ok(response):
            response.raise_for_status()

        items = json.loads(response.content)["Gservs"]
        for item in items:
            if len(item["Servicos"]) == 0:
                self.delete(item["GservsId"])
