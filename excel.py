#!/usr/bin/python
from excel_class import exsql
import sys

if len(sys.argv) == 2:
    workbook_name = sys.argv[1]
else:
    print("Arquivo não encontrado!!")
    exit()
try:
    # Abre o arquivo xlsx que contem os dados
    excelsql = exsql(workbook_name=workbook_name,
                     table_name="servicos",
                     sheet_name="serviço")
except FileNotFoundError:
    print("Arquivo não encontrado!")
    exit()
except xlrd.biffh.XLRDError:
    print("Arquivo não suportado!")
    exit()

excelsql.add_item(column_name="descricao",
               header_names=["descrição", "descricao", "descriçao"])
excelsql.add_item(column_name="grupo",
               header_names=["grupo"])
excelsql.add_item(column_name="valor",
               header_names=["valor"])
excelsql.add_item(column_name="comissao",
               header_names=["comissão", "comissao"])
excelsql.add_item(column_name="intevalo",
               header_names=["intervalo"])
excelsql.add_item(column_name="gasto",
               header_names=["gasto"])

excelsql.convert()
