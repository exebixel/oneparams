import re
from alive_progress import alive_bar
from oneparams.config import config_bar
from oneparams.excel.excel import Excel
from oneparams.api.client import ApiCliente
from oneparams.utils import wprint
import oneparams.config as config


def clientes(book, reset=False):
    one = ApiCliente()

    print("analyzing spreadsheet")

    ex = Excel(book=book, sheet_name="client", header_row=0)

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
    ex.add_column(key="aniversario",
                  name="aniversario",
                  types="date",
                  default=None,
                  required=False)

    ex.add_column(key="cep", name="cep", length=50)
    ex.add_column(key="endereco", name="endereco", length=50)
    ex.add_column(key="bairro", name="bairro", length=40)
    ex.add_column(key="complemento", name="complemento", length=50)
    ex.add_column(key="numeroEndereco",
                  name="numero",
                  default="",
                  types="float")

    ex.clean_columns()

    data = ex.data_all(check_row=checks, check_final=check_all)

    len_data = len(data)
    if reset:
        len_data += len(one.items)

    config_bar()
    with alive_bar(len_data) as bar:
        if reset:
            for i in list(one.items):
                one.delete(i)
                bar()

        for row in data:
            one.diff_item(row)
            bar()


def checks(row, data):
    erros = False

    if data["nomeCompleto"] is None:
        print("ERROR! in line {row}: empty name")
        erros = True

    data["numeroEndereco"] = re.sub(r'\.0$', '', str(data["numeroEndereco"]))

    if erros:
        raise Exception

    return data


def check_all(self, data):
    erros = False
    clis = {
        "nomeCompleto": "DUPLICATED! in lines {} and {}: Client {}",
        "email": "DUPLICATED! lines {} and {}: Client\'s email {}",
        "celular": "DUPLICATED! lines {} and {}: Client's phone {}"
    }

    for col, print_erro in clis.items():
        duplic = data[data.duplicated(keep=False, subset=col)]

        for i in duplic.loc[data[col].notnull()].index:
            for j in duplic.loc[data[col].notnull()].index:
                if (duplic.loc[i, col] == duplic.loc[j, col] and j != i):
                    message = print_erro.format(self.row(duplic.loc[i].name),
                                                self.row(duplic.loc[j].name),
                                                duplic.loc[i, col])
                    duplic = duplic.drop(index=i)

                    if config.RESOLVE_ERROS:
                        if col == "celular":
                            data.loc[i, col] = "00000000"
                        else:
                            data = data.drop(index=i)
                        wprint(message)
                    else:
                        print(message)
                        erros = True

                    break

    if erros:
        raise Exception

    if config.SKIP:
        one = ApiCliente()
        print("skipping clients already registered")
        for key, clis in one.items.items():
            data = data.drop(
                data[data.nomeCompleto == clis["nomeCompleto"]].index)

    return data
