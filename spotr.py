""" Spotr """

import logging
import os
import sys
import json

from rich.console import Console
from rich.logging import RichHandler

from Router import Router

route = Router()
console = Console()
log = logging.getLogger()

with open(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.json"),
    "r",
    encoding="utf-8",
) as f:
    CONFIG = json.load(f)

if eval(CONFIG["DEBUG"]):
    logging.basicConfig(
        level="NOTSET",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(markup=True, rich_tracebacks=True)],
    )
else:
    logging.basicConfig(
        level="INFO",
        datefmt="[%X]",
        format="%(message)s",
        handlers=[RichHandler(markup=True)],
    )

if len(sys.argv) < 2:
    getattr(route, "parse_functions")()
    sys.exit()

elif len(sys.argv) >= 2:
    sys.argv[1] = sys.argv[1].lower()
    if sys.argv[1] not in CONFIG["IGNORED_FUNCTIONS"]:
        try:
            sys.argv[2]
        except IndexError:
            try:
                getattr(route, sys.argv[1])()
            except AttributeError:
                message = f"[bold red]Invalid command - {sys.argv[1]}"
                ERROR: log = (
                    log.exception(message)
                    if eval(CONFIG["DEBUG"])
                    else log.error(message)
                )
            except TypeError:
                message = f"[bold red]Command needs input argument(s) - {sys.argv[1]}"
                ERROR: log = (
                    log.exception(message)
                    if eval(CONFIG["DEBUG"])
                    else log.error(message)
                )
        else:
            try:
                getattr(route, sys.argv[1])(*sys.argv[2:])
            except AttributeError:
                message = f"[bold red]Invalid argument - {sys.argv[1]}"
                EdRROR: log = (
                    log.exception(message)
                    if eval(CONFIG["DEBUG"])
                    else log.error(message)
                )
            except TypeError:
                message = (
                    f"[bold red]Command doesnt take second argument - {sys.argv[1]}"
                )
                ERROR: log = (
                    log.exception(message)
                    if eval(CONFIG["DEBUG"])
                    else log.error(message)
                )
    else:
        message = f"[bold red]Command in ignore list - {sys.argv[1]}"
        ERROR: log = (
            log.exception(message) if eval(CONFIG["DEBUG"]) else log.error(message)
        )