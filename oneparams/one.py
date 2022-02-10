#!/usr/bin/python
""" Modulo inicial do oneparams, as
abstrações dos parametros passados pela cli estão todas aqui
"""
import sys

import click
import pandas as pd

from oneparams import config
from oneparams.api.login import Login
from oneparams.excel.card import cards
from oneparams.excel.cliente import clientes
from oneparams.excel.colaborador import colaborador
from oneparams.excel.comissao import Comissao
from oneparams.excel.servicos import servico
from oneparams.reset import pw_reset

_global_options = [
    click.argument('worksheet', required=True, type=click.Path(exists=True)),
    click.option('-l',
                 '--login',
                 'login',
                 required=True,
                 type=str,
                 help="Email address to login"),
    click.option('-p',
                 '--password',
                 'password',
                 required=False,
                 type=str,
                 default='123456',
                 help="Access password (default = 123456)"),
    click.option('-e',
                 '--empresa',
                 'empresa',
                 required=True,
                 type=str,
                 help="Company name used to parametrization"),
    click.option('-eid',
                 '--empresa-id',
                 'empresa_id',
                 required=False,
                 type=int,
                 default=0,
                 help="Company id (if have some companies with same name)"),
    click.option('-f',
                 '--filial',
                 'filial',
                 required=False,
                 type=str,
                 help="Branch name used to parametrization"),
    click.option('-h',
                 '--header',
                 'header',
                 required=False,
                 type=int,
                 default=2,
                 help="line that will be used as header (default = 2)"),
    click.option('-W',
                 '--no-warning',
                 'warning',
                 required=False,
                 is_flag=True,
                 default=False,
                 help="Suppress warnings")
]
_reset_options = [
    click.option('-R',
                 '--reset',
                 'reset',
                 required=False,
                 is_flag=True,
                 default=False,
                 help="Delete or inactivate all services")
]
_error_options = [
    click.option('-E',
                 '--resolve-error',
                 'error',
                 required=False,
                 is_flag=True,
                 default=False,
                 help="Resolve erros (this can delete data)")
]
_skip_options = [
    click.option('-S',
                 '--skip',
                 'skip',
                 required=False,
                 is_flag=True,
                 default=False,
                 help='Skip items already registered')
]


def add_option(options):
    """ Adiciona parametros a um comando do click
    """

    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func

    return _add_options


def cli_login(kwargs: dict):
    """ Executa login na API
    """
    one = Login()
    one.login(nome_empresa=kwargs['empresa'],
              nome_filial=kwargs['filial'],
              email=kwargs['login'],
              senha=kwargs['password'],
              empresa_id=kwargs['empresa_id'])


def cli_file(worksheet: str) -> pd.ExcelFile:
    """ Verifica se o arquivo é valido
    """
    try:
        return pd.ExcelFile(worksheet)
    except FileNotFoundError as exp:
        sys.exit(exp)
    except ValueError as exp:
        sys.exit(exp)


def cli_config(error: bool = False, warning: bool = False, skip: bool = False):
    """ Setta as variaveis de configuração
    """
    config.RESOLVE_ERROS = error
    config.NO_WARNING = warning
    config.SKIP = skip


@click.group()
@click.version_option(config.VERSION)
def cli():
    """ Função padrão do click,
    necessária para ter os outros módulos
    """


@cli.command(help="Manipulating Services")
@add_option(_global_options)
@add_option(_reset_options)
def serv(**kwargs):
    """ Chama as funções do modulo de Serviço
    """
    cli_login(kwargs)
    book = cli_file(kwargs['worksheet'])
    cli_config(warning=kwargs['warning'])
    servico(book, reset=kwargs['reset'], header=kwargs['header'] - 1)


@cli.command(help="Manipulating Collaborators")
@add_option(_global_options)
def cols(**kwargs):
    """ Chama as funções do modulo de Colaborador
    """
    cli_login(kwargs)
    book = cli_file(kwargs['worksheet'])
    cli_config(warning=kwargs['warning'])
    colaborador(book, header=kwargs['header'] - 1)


@cli.command(help="Manipulating Cards")
@add_option(_global_options)
@add_option(_reset_options)
def card(**kwargs):
    """ Chama as funções do modulo de cartão
    """
    cli_login(kwargs)
    book = cli_file(kwargs['worksheet'])
    cli_config(warning=kwargs['warning'])
    cards(book, reset=kwargs['reset'], header=kwargs['header'] - 1)


@cli.command(help="Professional Committee Manipulation")
@add_option(_global_options)
@add_option(_reset_options)
@add_option(_error_options)
def comm(**kwargs):
    """ Chama as funções do modulo de Comissão
    """
    cli_login(kwargs)
    book = cli_file(kwargs['worksheet'])
    cli_config(warning=kwargs['warning'], error=kwargs['error'])
    Comissao(book, reset=kwargs['reset'], header=kwargs['header'] - 1)


@cli.command(help="Manipulating Clients")
@add_option(_global_options)
@add_option(_reset_options)
@add_option(_error_options)
@add_option(_skip_options)
def clis(**kwargs):
    """ Chama as funções do modulo de Clientes
    """
    cli_login(kwargs)
    book = cli_file(kwargs['worksheet'])
    cli_config(error=kwargs['error'],
               warning=kwargs['warning'],
               skip=kwargs['skip'])
    clientes(book, reset=kwargs['reset'], header=kwargs['header'] - 1)


@cli.command(help="Password Reset")
@click.argument('email', required=True, type=str)
@click.option('-k',
              '--key',
              'acess_key',
              envvar='ONE_RESET',
              required=True,
              type=str)
def reset(email: str, acess_key: str):
    """ Chama a função do modulo de resete de senha """
    pw_reset(email, acess_key)


if __name__ == "__main__":
    cli()
