# Importing necessary modules
import logging
import os
import sys
import json

# Importing console and logging utilities from rich module
from rich.console import Console
from rich.logging import RichHandler

# Importing the Router class from the Router module
from Router import Router

# Creating an instance of Router and Console
route = Router()
console = Console()
log = logging.getLogger()

# Loading configuration settings from the 'config.json' file
with open(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.json"),
    "r",
    encoding="utf-8",
) as f:
    CONFIG = json.load(f)

# Configuring logging settings based on the DEBUG configuration
if eval(CONFIG["DEBUG"]):
    # Detailed logging in debug mode
    logging.basicConfig(
        level="NOTSET",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(markup=True, rich_tracebacks=True)],
    )
else:
    # Standard logging for non-debug mode
    logging.basicConfig(
        level="INFO",
        datefmt="[%X]",
        format="%(message)s",
        handlers=[RichHandler(markup=True)],
    )

# Command-line argument handling
if len(sys.argv) < 2:
    # If no arguments are passed, display available functions
    getattr(route, "parse_functions")()
    sys.exit()
elif len(sys.argv) >= 2:
    # Lowercasing the first argument for command consistency
    sys.argv[1] = sys.argv[1].lower()
    if sys.argv[1] not in CONFIG["IGNORED_FUNCTIONS"]:
        try:
            sys.argv[2]  # Check for the presence of a second argument
        except IndexError:
            try:
                # Attempt to call the function without additional arguments
                getattr(route, sys.argv[1])()
            except AttributeError:
                # Handling invalid commands
                message = f"[bold red]Invalid command - {sys.argv[1]}"
                log.error(message) if not eval(CONFIG["DEBUG"]) else log.exception(
                    message
                )
            except TypeError:
                # Handling functions that require input arguments
                message = f"[bold red]Command needs input argument(s) - {sys.argv[1]}"
                log.error(message) if not eval(CONFIG["DEBUG"]) else log.exception(
                    message
                )
        else:
            try:
                # Attempt to call the function with additional arguments
                getattr(route, sys.argv[1])(*sys.argv[2:])
            except AttributeError:
                # Handling invalid arguments
                message = f"[bold red]Invalid argument - {sys.argv[1]}"
                log.error(message) if not eval(CONFIG["DEBUG"]) else log.exception(
                    message
                )
            except TypeError:
                # Handling functions that do not take a second argument
                message = (
                    f"[bold red]Command doesn't take second argument - {sys.argv[1]}"
                )
                log.error(message) if not eval(CONFIG["DEBUG"]) else log.exception(
                    message
                )
    else:
        # Handling commands that are in the ignore list
        message = f"[bold red]Command in ignore list - {sys.argv[1]}"
        log.error(message) if not eval(CONFIG["DEBUG"]) else log.exception(message)
