import sys

from api.colaborador import Colaboradores
from excel.excel import Excel
from utils import get_bool, get_cel


def colaborador(book):
    ex = Excel(book=book, sheet_name="profissiona")

    ex.add_column(key="nomeCompleto", name="nome")
    ex.add_column(key="email", name="email")
    ex.add_column(key="celular", name="celular")
    ex.add_column(key="perfil", name="perfil", default="colaborador")
    ex.add_column(key="agendavel",
                  name="agenda",
                  required=False,
                  default=False)
    ex.add_column(key="profissao",
                  name="profissao",
                  required=False,
                  default=None)
    ex.add_column(key="flagCliente",
                  name="cliente",
                  required=False,
                  default=True)
    ex.add_column(key="flagFornecedor",
                  name="fornecedor",
                  required=False,
                  default=True)
    ex.add_column(key="agendavelMobilidade",
                  name="mobilidade",
                  required=False,
                  default=True)

    one = Colaboradores()

    for row in range(2, ex.nrows):
        data = ex.data_row(row)

        data["celular"] = get_cel(data["celular"])

        data["agendavel"] = get_bool(data["agendavel"])
        if data["agendavel"] is None:
            print("unrecognized schedule option!!")
            sys.exit()

        one.colaborador(data)
