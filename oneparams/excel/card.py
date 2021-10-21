from alive_progress import alive_bar
from oneparams.api.cards import ApiCard
from oneparams.api.conta import ApiConta
from oneparams.api.operadora import Operadora
from oneparams.config import config_bar
from oneparams.excel.excel import Excel
from oneparams.utils import card_type


def cards(book, reset=False):
    one = ApiCard()
    print("analyzing spreadsheet")

    ex = Excel(book=book, sheet_name="cart")

    ex.add_column(key="descricao", name="nome", length=100)
    ex.add_column(key="debito_Credito", name="tipo")
    ex.add_column(key="comissao", name="comissao", default=0, types="float")
    ex.add_column(key="comissaoNegociadaOperadora",
                  name="cobrada",
                  default=0,
                  types="float")
    ex.add_column(key="operadoraCartaoId",
                  name="operadora",
                  default="Padrão",
                  length=50)
    ex.add_column(key="contasId",
                  name="conta",
                  required=False,
                  default="conta corrente")
    ex.clean_columns()

    data_all = ex.data_all(check_row=checks, check_final=check_all)

    operadora = Operadora()
    len_data = len(data_all)
    if reset:
        len_data += len(one.items)
        len_data += len(operadora.items)

    config_bar()
    with alive_bar(len_data) as bar:
        if reset:
            for i in list(one.items):
                one.delete_item(i)
                bar()
            for i in list(operadora.items):
                operadora.delete_item(i)
                bar()

        for row in data_all:
            one.diff_item(row)
            bar()


def checks(row, data):
    erros = False
    conta = ApiConta()

    data["contasId"] = conta.submodule_id(data["contasId"])
    if data["contasId"] == None:
        print(
            f'ERROR! in line {row}: Card {data["descricao"]} account not found'
        )
        erros = True

    if data["descricao"] is None:
        print("ERROR! in line {}: Name cannot be null".format(row))
        erros = True

    try:
        data["debito_Credito"] = card_type(data["debito_Credito"])
    except TypeError as exp:
        if data["debito_Credito"] is not None:
            print(f'ERROR! in line {row}: Card {data["descricao"]} {exp}')
            erros = True

        data["debito_Credito"] = "CD"

    if erros:
        raise Exception

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
