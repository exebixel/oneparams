from oneparams.excel.excel import Excel
from oneparams.api.client import Cliente
from oneparams.utils import check_email, deemphasize, get_cel


def clientes(book, reset=False):
    print("analyzing spreadsheet")

    ex = Excel(book=book, sheet_name="client")

    ex.add_column(key="ativoCliente",
                  name="ativoCliente",
                  default=True,
                  types="bool",
                  required=False)
    ex.add_column(key="nomeCompleto", name="nome", length=50)
    ex.add_column(key="email", name="email")
    ex.add_column(key="celular", name="celular")
    ex.add_column(key="cpf", name="cpf")
    ex.add_column(key="sexo", name="sexo")
    #  ex.add_column(key="aniversario", name="aniversario")
    ex.clean_columns()

    one = Cliente()

    data = ex.data_all(check_row=checks, check_final=check_all)
    for row in data:

        email_exist = True
        if row["email"] is None or row["celular"] is None:
            email_exist = False

        one.diff_item(row)


def checks(row, data):
    erros = False

    try:
        data["celular"] = get_cel(data["celular"])
    except ValueError as exp:
        if data["celular"] is None:
            print(
                f'WARNING! in line {row}: Client {data["nomeCompleto"]} has empty phone'
            )
        else:
            print(
                f'ERROR! in line {row}: Client {data["nomeCompleto"]} has {exp}'
            )
            erros = True

    if data["nomeCompleto"] is None:
        print("ERROR! in line {row}: empty name")
        erros = True
    if len(data["nomeCompleto"]) > 50:
        print(
            f'ERROR! in line {row}: Collaborator {data["nomeCompleto"]} name size {len(data["nomeCompleto"])} > 50'
        )
        erros = True

    if data["email"] != None:
        if not check_email(data["email"]):
            print(
                f'ERROR! in line {row}: Collaborator email {data["email"]} not valid'
            )
            erros = True
        else:
            if len(data["email"]) > 150:
                print(
                    f'ERROR! in line {row}: Collaborator email {data["email"]} size {len(data["email"])} > 150'
                )
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
