from oneparams.api.colaborador import Colaboradores
from oneparams.excel.excel import Excel


def colaborador(book):
    one = Colaboradores()
    print("analyzing spreadsheet")

    ex = Excel(book=book, sheet_name="profissiona")

    ex.add_column(key="nomeCompleto", name="nome", length=50)
    ex.add_column(key="email", name="email", types="email", length=50)
    ex.add_column(key="celular", name="celular", types="cel")
    ex.add_column(key="perfilId", name="perfil", default="colaborador")
    ex.add_column(key="agendavel",
                  name="agenda",
                  required=False,
                  default=False,
                  types="bool")
    ex.add_column(key="profissaoId",
                  name="profissao",
                  required=False,
                  default=None)
    ex.add_column(key="flagCliente",
                  name="cliente",
                  required=False,
                  default=True,
                  types="bool")
    ex.add_column(key="flagFornecedor",
                  name="fornecedor",
                  required=False,
                  default=True,
                  types="bool")
    ex.add_column(key="agendavelMobilidade",
                  name="mobilidade",
                  required=False,
                  default=True,
                  types="bool")
    ex.clean_columns()

    data = ex.data_all(check_row=checks, check_final=check_all)
    for row in data:
        one.diff_item(row)


def checks(row, data):
    erros = False

    if data["nomeCompleto"] is None:
        print(f"ERROR! in line {row}: empty name")
        erros = True

    one = Colaboradores()
    try:
        data = one.name_to_id(data)
    except Exception as exp:
        print(f'ERROR! in line {row}: {exp}')
        erros = True

    if erros:
        raise Exception

    return data


def check_all(self, data):
    erros = False
    cols = {
        "nomeCompleto":
        "ERROR! in lines {} and {}: Collaborator {} is duplicated",
        "email":
        "ERROR! in lines {} and {}: Collaborator\'s email {} is duplicated"
    }
    for col, print_erro in cols.items():
        duplic = data[data.duplicated(keep=False, subset=col)]
        for i in duplic.loc[data[col].notnull()].index:
            for j in duplic.loc[data[col].notnull()].index:
                if (duplic.loc[i, col] == duplic.loc[j, col] and j != i):
                    print(
                        print_erro.format(self.row(duplic.loc[i].name),
                                          self.row(duplic.loc[j].name),
                                          duplic.loc[i, col]))
                    duplic = duplic.drop(index=i)
                    erros = True
                    break
    if erros:
        raise Exception

    return data
