#!/usr/bin/python
import xlrd
import sys
from api.login import login
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

one = login()
access_token = one.login(
    empresaId="9467",
    filialId="9597",
    email="pilotolite@onebeleza.com.br",
    senha="123456"
)

book = xlrd.open_workbook(workbook_name)

servico(book, access_token)
# one.services(
#     nome = "teste",
#     preco = 20,
#     comissao = 50,
#     tempoExecucao = "00:30",
#     gservs = "Depilação"
# )
