import sys
from excel.excel import excel
from api.colaborador import colaboradores
from utils import *

def colaborador(book):
    ex = excel(
        book= book,
        sheet_name= "profissiona"
    )

    ex.add_column(key="nome", name="nome")
    ex.add_column(key="email", name="email")
    ex.add_column(key="celular", name="celular")
    ex.add_column(key="perfil", name="perfil",
                  default="colaborador")
    ex.add_column(key="agendavel", name="agenda",
                  default=False)
    ex.add_column(key="profissao", name="profissao",
                  default=None)

    one = colaboradores()

    for row in range(2, ex.nrows):
        data = ex.data_row(row)

        data["celular"] = get_cel(data["celular"])

        data["agendavel"] = get_bool(data["agendavel"])
        if data["agendavel"] == None:
            print("unrecognized schedule option!!")
            sys.exit()

        one.colaborador(data)
