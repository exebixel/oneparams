#!/usr/bin/env python
# -*- coding: utf-8 -*-

from alive_progress import config_handler

RESOLVE_ERROS = False
NO_WARNING = False
SKIP = False
VERSION = "0.3.0"

def config_bar():
    config_handler.set_global(stats=False, enrich_print=False)