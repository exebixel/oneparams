from oneparams.api.app import App
from oneparams.api.colaborador import Colaboradores
from oneparams.excel.excel import Excel
from oneparams.utils import deemphasize, get_cel


def colaborador(book, app_regist=False):
    print("analyzing spreadsheet")

    ex = Excel(book=book, sheet_name="profissiona")

    ex.add_column(key="nomeCompleto", name="nome")
    ex.add_column(key="email", name="email")
    ex.add_column(key="celular", name="celular")
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

    one = Colaboradores()
    app = App()

    data = ex.data_all(check_row=checks)
    for row in data:

        email_exist = True
        if row["email"] is None or row["celular"] is None:
            email_exist = False

        one.diff_item(row)
        if app_regist and email_exist:
            app.app(nome=row["nomeCompleto"],
                    email=row["email"],
                    celular=row["celular"])


def checks(row, data):
    erros = False

    try:
        data["celular"] = get_cel(data["celular"])
    except ValueError as exp:
        if data["celular"] is None:
            print(
                f'WARNING! on line {row}: Collaborator {data["nomeCompleto"]} has empty phone'
            )
        else:
            print(
                f'ERROR! in line {row}: Collaborator {data["nomeCompleto"]} has {exp}'
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

    try:
        if len(data["email"]) > 150:
            print(
                f'ERROR! in line {row}: Collaborator email {data["email"]} size {len(data["email"])} > 150'
            )
            erros = True
    except TypeError:
        print(
            f'WARNING! in line {row}: Collaborator {data["nomeCompleto"]} email is empty'
        )

    # for prev in previous:
    #     nome = deemphasize(data["nomeCompleto"])
    #     prev_nome = deemphasize(prev["data"]["nomeCompleto"])
    #     if nome == prev_nome:
    #         print(
    #             f'ERROR! in lines {row} and {prev["row"] + 1}: collaborator\'s {data["nomeCompleto"]} name is duplicated'
    #         )
    #         erros = True

    #     if data["email"] is not None:
    #         email = deemphasize(data["email"])
    #         prev_email = deemphasize(prev["data"]["email"])
    #         if email == prev_email:
    #             print(
    #                 f'ERROR! in lines {row} and {prev["row"] + 1}: collaborator\'s email {data["email"]} is duplicated'
    #             )
    #             erros = True

    one = Colaboradores()
    try:
        data = one.name_to_id(data)
    except Exception as exp:
        print(f'ERROR! in line {row}: {exp}')
        erros = True

    if erros:
        raise Exception

    return data
