from oneparams.api.base_diff import BaseDiff


class ApiConta(BaseDiff):
    items = {}
    first_get = False

    def __init__(self):
        super().__init__(
            key_id="contasId",
            key_name="nome",
            item_name="account",
            url_get_all="/OContas/ListaContasDetalhes"
        )

        if not ApiConta.first_get:
            self.get_all()
            ApiConta.first_get = True

    def get_all(self):
        items = super().get_all()
        ApiConta.items = {}
        for item in items:
            ApiConta.items[item[self.key_id]] = item
