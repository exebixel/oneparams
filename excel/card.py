from excel.excel import excel
from api.cards import card
from utils import *

def cards(book):

    ex = excel(
        book= book,
        sheet_name= "cart"
    )

    ex.add_column("descricao", "nome")
    ex.add_column("debito_Credito", "tipo")
    ex.add_column("comissao", "comissao")
    ex.add_column("comissaoNegociadaOperadora", "cobrada")
    ex.add_column("operadora", "operadora")

    one = card()

    for row in range(2, ex.nrows):
        data = ex.data_row(row)

        data["debito_Credito"] = card_type(data["debito_Credito"])
        one.card(data)