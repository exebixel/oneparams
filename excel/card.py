from api.cards import Card
from excel.excel import Excel
from utils import card_type


def cards(book):

    ex = Excel(book=book, sheet_name="cart")

    ex.add_column(key="descricao", name="nome")
    ex.add_column(key="debito_Credito", name="tipo")
    ex.add_column(key="comissao", name="comissao", default=0)
    ex.add_column(key="comissaoNegociadaOperadora", name="cobrada", default=0)
    ex.add_column(key="operadora", name="operadora", default="Padrão")
    ex.add_column(key="contas",
                  name="conta",
                  required=False,
                  default="conta corrente")

    one = Card()

    for row in range(2, ex.nrows):
        data = ex.data_row(row)

        data["debito_Credito"] = card_type(data["debito_Credito"])
        one.card(data)
