from oneparams.api.cards import apiCard
from oneparams.excel.excel import Excel
from oneparams.utils import card_type, deemphasize


def cards(book):

    ex = Excel(book=book, sheet_name="cart")

    ex.add_column(key="descricao", name="nome")
    ex.add_column(key="debito_Credito", name="tipo")
    ex.add_column(key="comissao", name="comissao", default=0, types="float")
    ex.add_column(key="comissaoNegociadaOperadora",
                  name="cobrada",
                  default=0,
                  types="float")
    ex.add_column(key="operadora", name="operadora", default="Padrão")
    ex.add_column(key="contas",
                  name="conta",
                  required=False,
                  default="conta corrente")

    one = apiCard()

    print("analyzing spreadsheet")
    data_all = ex.data_all(check_row=checks)
    for row in data_all:
        one.card(row)


def checks(row, data, previous):
    erros = False
    one = apiCard()
    data = one.name_to_id(data)

    if data["descricao"] is None:
        print("ERROR! in line {}: Name cannot be null".format(row + 1))
        erros = True

    try:
        data["debito_Credito"] = card_type(data["debito_Credito"])
    except TypeError as exp:
        if data["debito_Credito"] is not None:
            print("ERROR! in line {}: {}".format(row + 1, exp))
            erros = True

        data["debito_Credito"] = "CD"

    for prev in previous:
        descricao = deemphasize(data["descricao"])
        prev_descricao = deemphasize(prev["data"]["descricao"])
        if (descricao == prev_descricao
                and prev["data"]["debito_Credito"] in data["debito_Credito"]):
            print("ERROR! in lines {} and {}: Card is duplicated".format(
                row + 1, prev["row"] + 1))
            erros = True

    if erros:
        raise Exception

    if data["debito_Credito"] == "CD":
        data2 = {}
        for i, j in data.items():
            data2[i] = j

        data["debito_Credito"] = "C"
        data2["debito_Credito"] = "D"
        return [data, data2]
    return data
