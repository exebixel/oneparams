import sys

from oneparams.api.app import App
from oneparams.api.colaborador import Colaboradores
from oneparams.excel.excel import Excel
from oneparams.utils import get_cel


def colaborador(book, app_regist=False):
    ex = Excel(book=book, sheet_name="profissiona")

    ex.add_column(key="nomeCompleto", name="nome")
    ex.add_column(key="email", name="email")
    ex.add_column(key="celular", name="celular")
    ex.add_column(key="perfil", name="perfil", default="colaborador")
    ex.add_column(key="agendavel",
                  name="agenda",
                  required=False,
                  default=False,
                  types="bool")
    ex.add_column(key="profissao",
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

    one = Colaboradores()
    app = App()

    print("analyzing spreadsheet")
    data = ex.data_all(check_row=checks)
    for row in data:

        one.colaborador(row)
        if app_regist:
            app.app(nome=row["nomeCompleto"],
                    email=row["email"],
                    celular=row["celular"])


def checks(row, data):
    erros = False

    try:
        data["celular"] = get_cel(data["celular"])
    except ValueError as exp:
        print("ERROR! in line {}: {}".format(row + 1, exp))
        erros = True

    if data["nomeCompleto"] is None:
        print("ERROR! in line {}: empty name".format(row + 1))
        erros = True
    if data["email"] is None:
        print("ERROR! in line {}: empty email".format(row + 1))
        erros = True

    one = Colaboradores()
    try:
        data = one.name_to_id(data)
    except Exception as exp:
        print("ERROR! in line {}: {}".format(row + 1, exp))
        erros = True

    if erros:
        raise Exception

    return data
