from oneparams.api.base_diff import BaseDiff
from oneparams.utils import deemphasize


class ApiFormaPagamento(BaseDiff):
    items: dict = {
        2: {
            "formaDePagamentoId": 2,
            "descricao": "Cartão de Crédito"
        },
        3: {
            "formaDePagamentoId": 3,
            "descricao": "Cartão de Débito"
        },
        4: {
            "formaDePagamentoId": 4,
            "descricao": "PIX"
        },
        7: {
            "formaDePagamentoId": 7,
            "descricao": "PicPay"
        }
    }

    def __init__(self):
        super().__init__(key_id="formaDePagamentoId",
                         key_name="descricao",
                         item_name="forma de pagamento",
                         submodules={},
                         handle_errors={})

    def submodule_id(self, name: str) -> int:
        if deemphasize(name) == "d":
            name = "Débito"
        elif deemphasize(name) == "c":
            name = "Crédito"

        return self.search_item_by_name(name)
