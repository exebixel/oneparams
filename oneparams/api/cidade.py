from oneparams.api.submodule import SubModuleApi
from oneparams.utils import deemphasize, state_to_uf


class ApiCidade(SubModuleApi):

    items = {}

    def __init__(self) -> None:
        super().__init__(key_id="cidadesId",
                         key_name="descricao",
                         item_name="cidade",
                         url_search="/OCidadesEstados/PesquisaCidade")

    def item_id(self, data: dict) -> int:
        name = deemphasize(data[self.key_name])
        try:
            uf = state_to_uf(data["siglaEstado"])
        except ValueError:
            return 0

        try:
            for key, item in self.items.items():
                item_normalized = deemphasize(item[self.key_name])
                if (item_normalized == name
                        and uf == item["siglaEstado"]):
                    return key
        except KeyError:
            return 0
        return 0

    def submodule_id(self, city: str, state: str) -> dict:
        if city is None:
            return {
                self.key_id: None,
                "estadosId": None
            }

        try:
            state = state_to_uf(state)
        except ValueError as e:
            raise ValueError(str(e))

        id = self.item_id({
            self.key_name: city,
            "siglaEstado": state
        })
        if id != 0:
            return {
                self.key_id: id,
                "estadosId": self.items[id]["estadosId"]
            }

        # pesquisa na api
        self.search(city)
        id = self.item_id({
            self.key_name: city,
            "siglaEstado": state
        })
        if id != 0:
            return {
                self.key_id: id,
                "estadosId": self.items[id]["estadosId"]
            }

        raise ValueError(f"{self.item_name} {city} not found!")
