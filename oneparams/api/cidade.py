from oneparams.api.submodule import SubModuleApi
from oneparams.utils import deemphasize, state_to_uf


class ApiCidade(SubModuleApi):

    items: dict = {}
    know_erros: list = []
    name_list: dict = {}

    def __init__(self) -> None:
        super().__init__(key_id="cidadesId",
                         key_name="descricao",
                         item_name="cidade",
                         keys_search=["descricao"],
                         url_search="/OCidadesEstados/PesquisaCidade",
                         key_search_term="descricao")

    def item_id(self, data: dict) -> int:
        try:
            uf_state = state_to_uf(data["siglaEstado"])
        except ValueError:
            return 0

        for key in self.keys_search:
            name = deemphasize(data[key])
            try:
                for item_id in self.name_list[key][name]:
                    uf_state_item = self.items[item_id]["siglaEstado"]
                    if uf_state_item == uf_state:
                        return item_id
            except KeyError:
                pass
        return 0

    def submodule_id(self, city: str, state: str) -> dict:
        if city is None:
            return {self.key_id: None, "estadosId": None}

        try:
            state = state_to_uf(state)
        except ValueError as exp:
            raise ValueError(str(exp)) from exp

        item_id = self.item_id({self.key_name: city, "siglaEstado": state})
        if item_id != 0:
            return {
                self.key_id: item_id,
                "estadosId": self.items[item_id]["estadosId"]
            }

        for value in self.know_erros:
            if (value["city"] == city and value["state"] == state):
                raise ValueError(
                    f"{self.item_name} '{city}/{state}' not found!")

        # pesquisa na api
        self.search(city)
        item_id = self.item_id({self.key_name: city, "siglaEstado": state})
        if item_id != 0:
            return {
                self.key_id: item_id,
                "estadosId": self.items[item_id]["estadosId"]
            }

        self.know_erros.append({"city": city, "state": state})
        raise ValueError(f"{self.item_name} '{city}/{state}' not found!")
