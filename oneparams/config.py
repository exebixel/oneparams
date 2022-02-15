""" Informações globais de configuração
"""

from alive_progress import config_handler

RESOLVE_ERROS = False
NO_WARNING = False
SKIP = False
VERSION = "0.3.4.1"


def config_bar():
    """ Configuração padrão da barra de progresso
    """
    config_handler.set_global(stats=False, enrich_print=False, spinner=None)


class CheckException(Exception):
    """ Exception especifica para algum erro de verificação do modulo de excel
    """
