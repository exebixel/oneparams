from oneparams.api.gservs import Gservis
from oneparams.api.servicos import Servicos
from oneparams.excel.excel import Excel
from oneparams.utils import deemphasize


def servico(book, reset=False):
    print("analyzing spreadsheet")

    ex = Excel(book, "servico")

    ex.add_column(key="flagAtivo", name="ativo", required=False, default=True)
    ex.add_column(key="descricao", name="nome")
    ex.add_column(key="gservId", name="grupo")
    ex.add_column(key="preco", name="valor", default=0, types="float")
    ex.add_column(key="comissao", name="comissao", default=0, types="float")
    ex.add_column(key="tempoExecucao",
                  name="execucao",
                  default="00:30:00",
                  types="time")
    ex.add_column(key="custosGerais",
                  name="custo",
                  required=False,
                  default=0,
                  types="float")
    ex.add_column(key="intervaloMarcacao",
                  name="intervalo",
                  required=False,
                  default="00:10:00",
                  types="time")
    ex.add_column(key="permiteEncaixe",
                  name="encaixe",
                  required=False,
                  default=True,
                  types="bool")
    ex.add_column(key="permiteSimultaneidade",
                  name="simultaniedade",
                  required=False,
                  default=True,
                  types="bool")
    ex.add_column(key="valPercComissao",
                  name="tipo comissao",
                  required=False,
                  default="P")
    ex.add_column(key="valPercCustos",
                  name="tipo custo",
                  required=False,
                  default="P")
    ex.clean_columns()

    one = Servicos()
    data = ex.data_all(check_row=checks, check_final=check_all)

    if reset:
        one.delete_all()

    for row in data:
        one.diff_item(row)

    grupo = Gservis()
    grupo.all_Gservis()
    grupo.clear()


def checks(row, data):
    erros = False
    if data["descricao"] is None:
        print(f'ERROR! in line {row}: empty name')
        erros = True
    if len(data["descricao"]) > 50:
        print(
            f'ERROR! in line {row}: Service {data["descricao"]} name size {len(data["descricao"])}/50'
        )
        erros = True
    if data["gservId"] is None:
        print(
            f'ERROR! in line {row}: Service {data["descricao"]} have empty group'
        )
        erros = True

    comissao = data["comissao"]
    if comissao <= 1:
        data["comissao"] = comissao * 100

    if erros:
        raise Exception

    one = Servicos()
    return one.name_to_id(data)


def check_all(self, data):
    erros = False
    duplic = data[data.duplicated(keep=False, subset=["descricao"])]
    for i in duplic.index:
        for j in duplic.index:
            if (duplic.loc[i, "descricao"] == duplic.loc[j, "descricao"]
                    and j != i):
                print("ERROR! in lines {} and {}: Service {} is duplicated".
                      format(self.row(duplic.loc[i].name),
                             self.row(duplic.loc[j].name),
                             duplic.loc[i, 'descricao']))
                duplic = duplic.drop(index=i)
                erros = True
                break
    if erros:
        raise Exception

    return data
