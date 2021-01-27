import pandas as pd
from oneparams.api.commission import Commission
from oneparams.excel.excel import Excel
from oneparams.utils import get_names


def comissao(book, reset=False):
    print("analyzing spreadsheet")

    ex = Excel(book, "servico")
    ex.add_column(key="servico", name="nome")
    ex.add_column(key="servId",
                  name="servico id",
                  required=False,
                  types="float",
                  default=0)
    ex.add_column(key="ServicoValorComissao",
                  name="comissao",
                  default=0,
                  types="float")
    ex.add_column(key="cols", name="profissionais")
    ex.add_column(key="colsId", required=False, types="float", name="colsId")
    ex.clean_columns()
    ex.add_row_column()

    one = Commission()

    data_all = ex.data_all(check_final=checks_comm)

    if reset:
        one.delete_all()

    for row in data_all:
        one.comissao(row)


erros = False


def checks_comm(self, data):
    api = Commission()

    data = data.loc[data["cols"].notnull()]
    data = data.apply(get_serv_id, axis=1)

    final_data = pd.DataFrame()
    for i in data.iterrows():
        final_data = final_data.append(cols_names_to_id(i[1]))

    if erros:
        raise Exception
    return final_data


def get_serv_id(data):
    api = Commission()
    data["servId"] = api.serv.item_id({"descricao": data["servico"]})
    if data["servId"] == 0:
        print("ERROR!! in line {}: Service {} not found".format(
            data["row"], data["servico"]))
        erros = True
    return data


def cols_names_to_id(data):
    cols = get_names(data["cols"])

    api = Commission()

    ids = []
    for i in cols:
        try:
            ids.append(api.cols.search_item_by_name(i))
        except ValueError as exp:
            print("ERROR!! in line {}: {}".format(data["row"], exp))
            erros = True

    return pd.DataFrame({
        "servico": data["servico"],
        "servId": data["servId"],
        "cols": cols,
        "colsId": ids,
        "ServicoValorComissao": data["ServicoValorComissao"],
        "ativo": True,
        "row": data["row"]
    })
