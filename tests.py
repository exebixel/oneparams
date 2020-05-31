import xlrd
import sys
from one_api import one_api
from servicos import servico

if len(sys.argv) == 2:
    workbook_name = sys.argv[1]
else:
    print("Arquivo não encontrado!!")
    exit()
try:
    pass
except FileNotFoundError:
    print("Arquivo não encontrado!")
    exit()
except xlrd.biffh.XLRDError:
    print("Arquivo não suportado!")
    exit()

one = one_api()
access_token = one.login(
    empresaId="9324",
    filialId="9448",
    email="ezequielnat7@gmail.com",
    senha="123456"
)

book = xlrd.open_workbook("excel.xlsx")

servico(book, access_token)
# one.services(
#     nome = "teste",
#     preco = 20,
#     comissao = 50,
#     tempoExecucao = "00:30",
#     gservs = "Depilação"
# )
