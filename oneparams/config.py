""" Informações globais de configuração
"""
from alive_progress import config_handler

RESOLVE_ERROS = False
NO_WARNING = False
SKIP = False
VERSION = "0.3.5.2"


def config_bar_api():
    """ Configuração padrão da barra de progresso para API
    """
    config_handler.set_global(bar="smooth",
                              stats=True,
                              enrich_print=False,
                              spinner=None,
                              receipt=True,
                              elapsed=True)


def config_bar_excel():
    """ Configuração padrão da barra de progresso os módulos de excel
    """
    config_handler.set_global(bar=None,
                              spinner=False,
                              receipt=False,
                              enrich_print=False,
                              stats=False,
                              elapsed=False)


class CheckException(Exception):
    """ Exception especifica para algum erro de verificação do modulo de excel
    """
