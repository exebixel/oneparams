import sys
from excel.excel import excel
from api.colaborador import colaboradores
from utils import *

def colaborador(book):
    ex = excel(
        book= book,
        sheet_name= "profissiona"
    )

    ex.add_column("nome", "nome")
    ex.add_column("email", "email")
    ex.add_column("celular", "celular")
    ex.add_column("perfil", "perfil")
    ex.add_column("agendavel", "agenda")
    ex.add_column("profissao", "profissao")

    one = colaboradores()

    for row in range(2, ex.nrows):
        data = ex.data_row(row)

        data["celular"] = get_cel(data["celular"])

        if string_normalize(data["agendavel"]) == "sim":
            data["agendavel"] = True
        elif string_normalize(data["agendavel"]) == "nao":
            data["agendavel"] = False
        else:
            print("unrecognized schedule option!!")
            sys.exit()

        one.colaborador(data)
