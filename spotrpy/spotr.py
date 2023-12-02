""" Spotr """

import logging
import os
import sys
import json
from rich.console import Console
from rich.logging import RichHandler
from .Router import Router


class Spotr:
    """Spotr"""

    def __init__(self, router, config):
        self.router = router
        self.console = Console()
        self.log = logging.getLogger()
        self.config = config

        if eval(self.config["DEBUG"]):
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

    def run(self, args):
        """Run spotr command"""
        if len(args) == 0:
            getattr(self.router, "parse_functions")()
            sys.exit()
        if len(args) >= 1:
            sys.argv[1] = sys.argv[1].lower()
            if sys.argv[1] not in self.config["IGNORED_FUNCTIONS"]:
                try:
                    sys.argv[2]
                except IndexError:
                    try:
                        getattr(self.router, args[0])()
                    except AttributeError:
                        message = f"[bold red]Invalid command - {args[0]}"
                        self.log = (
                            self.log.exception(message)
                            if eval(self.config["DEBUG"])
                            else self.log.error(message)
                        )
                    except TypeError:
                        message = (
                            f"[bold red]Command needs input argument(s) - {args[0]}"
                        )
                        self.log = (
                            self.log.exception(message)
                            if eval(self.config["DEBUG"])
                            else self.log.error(message)
                        )
                else:
                    try:
                        getattr(self.router, args[0])(*args[1:])
                    except AttributeError:
                        message = f"[bold red]Invalid argument - {args[0]}"
                        self.log = (
                            self.log.exception(message)
                            if eval(self.config["DEBUG"])
                            else self.log.error(message)
                        )
                    except TypeError:
                        message = (
                            f"[bold red]Command doesnt take second argument - {args[0]}"
                        )
                        self.log = (
                            self.log.exception(message)
                            if eval(self.config["DEBUG"])
                            else self.log.error(message)
                        )
            else:
                message = f"[bold red]Command in ignore list - {args[1]}"
                self.log = (
                    self.log.exception(message)
                    if eval(self.config["DEBUG"])
                    else self.log.error(message)
                )

def main():
    """main"""
    router = Router()
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.json"),
        "r",
        encoding="utf-8",
    ) as f:
        config = json.load(f)
    spotr = Spotr(router, config)
    spotr.run(sys.argv[1:])


if __name__ == "__main__":
    main()
