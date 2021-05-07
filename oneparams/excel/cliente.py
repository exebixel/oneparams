from oneparams.excel.excel import Excel
from oneparams.api.client import Cliente
from oneparams.utils import check_email, get_cel, wprint, eprint
import oneparams.config as config


def clientes(book, reset=False):
    one = Cliente()

    print("analyzing spreadsheet")

    ex = Excel(book=book, sheet_name="client")

    ex.add_column(key="ativoCliente",
                  name="ativoCliente",
                  default=True,
                  types="bool",
                  required=False)
    ex.add_column(key="nomeCompleto", name="nome", length=50)
    ex.add_column(key="email", name="email", types="email")
    ex.add_column(key="celular", name="celular", types="cel")
    ex.add_column(key="cpf", name="cpf")
    ex.add_column(key="sexo", name="sexo")
    #  ex.add_column(key="aniversario", name="aniversario")
    ex.clean_columns()

    data = ex.data_all(check_row=checks, check_final=check_all)
    for row in data:
        one.diff_item(row)


def checks(row, data):
    erros = False

    if data["nomeCompleto"] is None:
        print("ERROR! in line {row}: empty name")
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
