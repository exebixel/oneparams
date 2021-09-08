from oneparams.api.gservs import Gservis
from oneparams.api.servicos import Servicos
from oneparams.excel.excel import Excel


def servico(book, reset=False):
    """
    Book: planilha com todos os dados \n
    reset: True se todos os serviços do sistema
    serão excluídos para cadastrar os serviços da planilha \n

    Nessa função tem toda a descrição do json que vai ser enviado
    para as rotas de cadastro do sistema

    Return None
    """
    one = Servicos()
    print("analyzing spreadsheet")

    ex = Excel(book, "servico")

    ex.add_column(key="flagAtivo", name="ativo", required=False, default=True)
    ex.add_column(key="descricao", name="nome", length=50)
    ex.add_column(key="gservId", name="grupo")
    ex.add_column(key="preco", name="valor", default=1, types="float")
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

    data = ex.data_all(check_row=checks, check_final=check_all)

    if reset:
        one.delete_all()

    for row in data:
        one.diff_item(row)

    grupo = Gservis()
    grupo.all_Gservis()
    grupo.clear()


def checks(row, data):
    """
    row: linha da planilha \n
    data: dados da linha da planilha \n

    verificações especificas de serviços,
    isso linha a linha, de forma individual

    return data \n
    raise Exception: caso ocorra algum erro durante
    as verificações \n
    """
    erros = False
    if data["descricao"] is None:
        print(f'ERROR! in line {row}: empty name')
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
    """
    self: referencia da classe excel \n
    data: data frame com todos os dados da planilha \n

    Verificações 'globais', que necessitam de todos os
    dados da planilha, principalmente duplicações

    return data \n
    raise Exception: caso tenha algum erro durante as
    verificações \n

    """
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
