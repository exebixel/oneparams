from oneparams.api.submodule import SubModuleApi


class ApiLinhaProduto(SubModuleApi):

    items: dict = {}

    def __init__(self) -> None:
        super().__init__(
            key_id="linhasId",
            key_name="descricao",
            item_name="linha",
            url_search="/Linhas/PesquisarLinhas",
            url_create="/Linhas/CreateLinhas",
            url_delete="/Linhas/DeleteLinha"
        )
