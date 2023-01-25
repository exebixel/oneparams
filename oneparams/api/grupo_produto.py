from oneparams.api.base_diff import BaseDiff


class ApiGrupoProduto(BaseDiff):

    items: dict = {}
    name_list: dict = {}
    first_get: bool = False

    def __init__(self):
        super().__init__(key_id="grupoId",
                         key_name="descricao",
                         item_name="grupo",
                         keys_search=["descricao"],
                         url_get_all="/OGruposProdutos/GetGruposProdutos",
                         url_create="/OGruposProdutos/CriarGruposProdutos")

        if not ApiGrupoProduto.first_get:
            self.get_all()
            ApiGrupoProduto.first_get = True

    def get_all(self) -> dict:
        ApiGrupoProduto.items = {}
        ApiGrupoProduto.name_list = {}
        return super().get_all()

    def add_item(self, data: dict, response: dict) -> int:
        response["data"] = response["data"]["grupoid"]
        return super().add_item(data, response)
