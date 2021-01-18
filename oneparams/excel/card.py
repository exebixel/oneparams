from oneparams.api.cards import apiCard
from oneparams.api.conta import Conta
from oneparams.api.operadora import Operadora
from oneparams.excel.excel import Excel
from oneparams.utils import card_type, deemphasize


def cards(book, reset=False):
    print("analyzing spreadsheet")

    ex = Excel(book=book, sheet_name="cart")

    ex.add_column(key="descricao", name="nome")
    ex.add_column(key="debito_Credito", name="tipo")
    ex.add_column(key="comissao", name="comissao", default=0, types="float")
    ex.add_column(key="comissaoNegociadaOperadora",
                  name="cobrada",
                  default=0,
                  types="float")
    ex.add_column(key="operadoraCartaoId", name="operadora", default="Padrão")
    ex.add_column(key="contasId",
                  name="conta",
                  required=False,
                  default="conta corrente")
    ex.clean_columns()

    data_all = ex.data_all(check_row=checks, check_final=check_all)

    one = apiCard()
    if reset:
        one.delete_all()
        operadora = Operadora()
        operadora.delete_all()

    for row in data_all:
        one.diff_item(row)


def checks(row, data):
    erros = False
    conta = Conta()

    data["contasId"] = conta.return_id(data["contasId"])
    if data["contasId"] == None:
        print(
            f'ERROR! in line {row}: Card {data["descricao"]} account not found'
        )
        erros = True

    if data["descricao"] is None:
        print("ERROR! in line {}: Name cannot be null".format(row))
        erros = True
    if len(data["descricao"]) > 100:
        print(
            f'ERROR! in line {row}: Card {data["descricao"]} name size {len(data["descricao"])} > 100'
        )
        erros = True

    if len(data["operadoraCartaoId"]) > 50:
        print(
            f'ERROR! in line {row}: Card {data["descricao"]} card operator size {len(data["operadoraCartaoId"])} > 50'
        )
        erros = True

    try:
        data["debito_Credito"] = card_type(data["debito_Credito"])
    except TypeError as exp:
        if data["debito_Credito"] is not None:
            print(f'ERROR! in line {row}: Card {data["descricao"]} {exp}')
            erros = True

        data["debito_Credito"] = "CD"

    # for prev in previous:
    #     descricao = deemphasize(data["descricao"])
    #     prev_descricao = deemphasize(prev["data"]["descricao"])
    #     if (descricao == prev_descricao
    #             and prev["data"]["debito_Credito"] in data["debito_Credito"]):
    #         print(
    #             f'ERROR! in lines {row} and {prev["row"] + 1}: Card {data["descricao"]} is duplicated'
    #         )
    #         erros = True

    if erros:
        raise Exception

    # if data["debito_Credito"] == "CD":
    #     data2 = {}
    #     for i, j in data.items():
    #         data2[i] = j

    #     data["debito_Credito"] = "C"
    #     data2["debito_Credito"] = "D"
    #     return [data, data2]
    return data


def check_all(self, data):
    erros = False
    duplic = data[data.duplicated(keep=False,
                                  subset=["descricao", "debito_Credito"])]
    if not duplic.empty:
        erros = True
        duplic.apply(lambda x: print(
            f'ERROR! in line {self.row(x.name)}: Card {x["descricao"]} is duplicated'
        ),
                     axis=1)

    if erros:
        raise Exception

    cd = data.loc[data["debito_Credito"] == "CD"]
    for i, row in cd.iterrows():
        copy = row.copy()
        row["debito_Credito"] = "D"
        copy["debito_Credito"] = "C"
        data = data.append([row, copy])
    data = data[data["debito_Credito"] != "CD"]
    data = data.sort_index("index")

    return data
