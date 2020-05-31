import xlrd
import re
import sys
from  datetime import time
from one_api import one_api
from excel_class import excel
from utils import *
from servicos import *

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
one.login(
    empresaId="9324",
    filialId="9448",
    email="ezequielnat7@gmail.com",
    senha="123456"
)

book = xlrd.open_workbook("excel.xlsx")

servico(book)
