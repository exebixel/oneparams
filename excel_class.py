#!/usr/bin/python
import xlrd
import re
import sys
from utils import *

class excel():

    def sheet_index(book, sheet_name):
        cont = 0
        for names in book.sheet_names():
            names = string_normalize(names)
            if ( re.search(sheet_name, names, re.IGNORECASE) ):
                break
            cont+=1
        else:
            return -1
        return cont

    def column_index(sheet, column_name):
        cont = 0
        for header in range(sheet.ncols):
            header_name = sheet.cell_value(rowx=1, colx=header)
            header_name = string_normalize(header_name)

            if ( re.search(column_name, header_name, re.IGNORECASE) ):
                break
            cont+=1
        else:
            return -1
        return cont


    def __init__(self, workbook_name, table_name, sheet_name):
        self.__columns = []
        self.__header_tests = []
        self.__type = []
        self.__table_name = table_name
        self.__workbook_name = workbook_name
        self.__sheet_name = sheet_name

    def add_item(self, column_name, header_names, item_type=None):
        self.__columns.append(column_name)
        self.__header_tests.append(header_names)
        self.__type.append(item_type)

    def convert(self):
        book = xlrd.open_workbook(self.__workbook_name)
        # Encontra a planilha com as dados dos serviços 
        # que devend ser castrados
        cont=0
        for names in book.sheet_names():
            if ( re.search(self.__sheet_name, names, re.IGNORECASE) ):
                break
            cont+=1
        else:
            # Se a planilha não for encontrada o programa encerra
            print("Não foi possivel encontrar a planilha")
            exit()

        # Pega a planilha requerida acima 
        sh = book.sheet_by_index(cont)

        # array para gruardar as posições dos cabeçarios
        # as posições do array são iguais as posições dos testes
        header_index = []
        # ANALIZA OS CABEÇARIOS 
        # os dois primeiros for são para os testes
        # por que é uma matriz de palavras de teste
        # para permitir que tenham mais de uma palavra 
        # testada para encontrar um cabeçario
        for test in self.__header_tests:
            for test in test:
                # Indica se o cabeçario com o teste ja foi encontrado
                # se sim, passe para o proximo teste
                # isso é pra evitar operações desnecesarias
                cont = 0
                # percorre todos os cabeçarios 
                # testando para pode saber o que é o que
                for header in range(sh.ncols):
                    # realiza o teste propriamente dito
                    # testa sé a palavra se encontra um algum cabeçario
                    header_name = sh.cell_value(rowx=0, colx=header)
                    if ( re.search(test, header_name, re.IGNORECASE) ):
                        # se for encontrado pega o index (número) do cabeçario
                        # assim é possivel deixar isso "organizado"
                        # para quando for preciso pesquisar alguma informação na planilha
                        header_index += [header]
                        cont = 1
                        break
                if cont == 1:
                    break
        # se não for encontrado nenhum cabeçario no teste,
        # ele vai ser -1 por que não tem index com esse número
        else:
            header_index += [-1]

        # cols_format = ""
        # for i in self.__columns:
        #     if cols_format != "":
        #         cols_format = cols_format + ", " + i 
        #     else:
        #         cols_format = i

        # with open("excel.sql", "w") as arq:
        #     for i in range(1, sh.nrows):
        #         value = ""
        #         for h in header_index:
        #             if h != -1 and value != "":
        #                 value = value + ", " + str( sh.cell_value(rowx=i, colx=h) )
        #             elif value == "":
        #                 value = sh.cell_value(rowx=i, colx=h)

        #         sql = f'INSERT INTO {self.__table_name}( {cols_format} ) \n\tVALUES ( {value} );\n\n'
        #         arq.write(sql)
