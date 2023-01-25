from oneparams.api.base_diff import BaseDiff


class ApiLinhaProduto(BaseDiff):

    items: dict = {}
    name_list: dict = {}
    first_get: bool = False

    def __init__(self):
        super().__init__(key_id="linhasId",
                         key_name="descricao",
                         item_name="linha",
                         keys_search=["descricao"],
                         url_get_all="/Linhas/GetTodasLinhas",
                         url_create="/Linhas/CreateLinhas",
                         url_delete="/Linhas/DeleteLinha")

        if not ApiLinhaProduto.first_get:
            self.get_all()
            ApiLinhaProduto.first_get = True

    def get_all(self) -> dict:
        ApiLinhaProduto.items = {}
        ApiLinhaProduto.name_list = {}
        return super().get_all()
