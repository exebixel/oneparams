#!/usr/bin/python
import argparse
import sys

import pandas as pd

from oneparams.api.login import login
from oneparams.args import parse_base
from oneparams.excel.card import cards
from oneparams.excel.colaborador import colaborador
from oneparams.excel.comissao import Comissao
from oneparams.excel.servicos import servico
from oneparams.excel.cliente import clientes
import oneparams.config as config


def one():
    parser = argparse.ArgumentParser(description="One system parameterizer")
    sub = parser.add_subparsers(dest="cmd")
    sub.required = True

    serv = sub.add_parser("serv", help="manipulating services")
    serv = parse_base(serv)
    serv.add_argument("-R",
                      "--reset",
                      action="store_true",
                      help="Delete or inactivate all services")

    cols = sub.add_parser("cols", help="manipulating collaborators")
    cols = parse_base(cols)

    clis = sub.add_parser("clis", help="manipulating clients")
    clis = parse_base(clis)
    clis.add_argument("-R",
                      "--reset",
                      action="store_true",
                      help="Delete or inactivate all clients")
    clis.add_argument("-E",
                      "--no-erros",
                      action="store_true",
                      help="Resolve erros (this can delete data)")
    clis.add_argument("-S",
                      "--skip",
                      action="store_true",
                      help="Skip items already registered")

    card_parse = sub.add_parser("card", help="manipulating cards")
    card_parse = parse_base(card_parse)
    card_parse.add_argument("-R",
                            "--reset",
                            action="store_true",
                            help="Delete or inactivate all cards")

    com_parse = sub.add_parser("comm",
                               help="Professional committee manipulation")
    com_parse = parse_base(com_parse)
    com_parse.add_argument("-R",
                           "--reset",
                           action="store_true",
                           help="Delete all professional committee")

    args = parser.parse_args()

    try:
        book = pd.ExcelFile(args.worksheet)
    except FileNotFoundError as exp:
        print(exp)
        sys.exit()
    except ValueError as exp:
        print(exp)
        sys.exit()

    one = login()
    one.login(nome_empresa=args.empresa,
              nome_filial=args.filial,
              email=args.login,
              senha=args.password,
              empresa_id=args.empresaid)

    config.NO_WARNING = args.no_warning

    if args.cmd == "serv":
        servico(book, reset=args.reset)

    if args.cmd == "cols":
        colaborador(book)

    if args.cmd == "clis":
        config.RESOLVE_ERROS = args.no_erros
        config.SKIP = args.skip
        clientes(book, reset=args.reset)

    if args.cmd == "card":
        cards(book, reset=args.reset)

    if args.cmd == "comm":
        Comissao(book, reset=args.reset)


def main():
    try:
        one()
    except KeyboardInterrupt:
        print("\nQuiting...")


if __name__ == "__main__":
    main()
