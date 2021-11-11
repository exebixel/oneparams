from oneparams.api.base_diff import BaseDiff


class Gservis(BaseDiff):
    items = {}
    first_get = False

    def __init__(self):
        super().__init__(
            key_id="id",
            key_name="nome",
            item_name="service group",
            url_get_all="/OGservsServicos/GservsServicos",
            url_create="/Gservs/CreateGServsLight",
            url_delete="/Gservs/DeleteGservs"
        )

        if not Gservis.first_get:
            self.get_all()
            Gservis.first_get = True

    def get_all(self):
        items = super().get_all()
        Gservis.items = {}
        for gservs in items["Gservs"]:
            Gservis.items[gservs["GservsId"]] = {
                self.key_id: gservs["GservsId"],
                self.key_name: gservs["GservsNome"],
                "cont": len(gservs["Servicos"])
            }

    def add_item(self, data: dict, response: dict) -> int:
        data["cont"] = 0
        return super().add_item(data, response)

    def clear(self):
        for key in list(self.items):
            if self.items[key]["cont"] == 0:
                self.delete(key)
