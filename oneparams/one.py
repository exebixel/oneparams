#!/usr/bin/python
import argparse
import sys

import xlrd
from oneparams.api.cards import Card
from oneparams.api.commission import Commission
from oneparams.api.login import login
from oneparams.api.servicos import Servicos
from oneparams.args import parse_base
from oneparams.excel.card import cards
from oneparams.excel.colaborador import colaborador
from oneparams.excel.comissao import comissao
from oneparams.excel.servicos import servico


def one():
    parser = argparse.ArgumentParser(description="One system parameterizer")
    sub = parser.add_subparsers(dest="cmd")
    sub.required = True

    serv = sub.add_parser("serv", help="manipulating services")
    serv.add_argument("-R",
                      "--reset",
                      action="store_true",
                      help="Delete or inactivate all services")
    serv = parse_base(serv)

    cols = sub.add_parser("cols", help="manipulating collaborators")
    cols.add_argument("-a",
                      "--app",
                      action="store_true",
                      help="Register collaborator in the app")
    cols = parse_base(cols)

    card_parse = sub.add_parser("card", help="manipulating cards")
    card_parse.add_argument("-R",
                            "--reset",
                            action="store_true",
                            help="Delete or inactivate all cards")
    card_parse = parse_base(card_parse)

    com_parse = sub.add_parser("comm",
                               help="Professional committee manipulation")
    com_parse.add_argument("-R",
                           "--reset",
                           action="store_true",
                           help="Delete all professional committee")
    com_parse = parse_base(com_parse)

    args = parser.parse_args()

    try:
        book = xlrd.open_workbook(args.worksheet)
    except FileNotFoundError:
        print("File not found!!")
        sys.exit()
    except xlrd.biffh.XLRDError:
        print("Unsupported file!!")
        sys.exit()

    one = login()
    one.login(nome_empresa=args.empresa,
              nome_filial=args.filial,
              email=args.login,
              senha=args.password)

    if args.cmd == "serv":
        if args.reset:
            serv = Servicos()
            serv.delete_all()
        servico(book)

    if args.cmd == "cols":
        colaborador(book, args.app)

    if args.cmd == "card":
        if args.reset:
            cd = Card()
            cd.delete_all()
            cd.operadora.delete_all()
        cards(book)

    if args.cmd == "comm":
        if args.reset:
            comm = Commission()
            comm.delete_all()
        comissao(book)


def main():
    try:
        one()
    except KeyboardInterrupt:
        print("Quiting...")


if __name__ == "__main__":
    main()
