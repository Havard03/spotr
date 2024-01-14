import logging

from rich.console import Console
from rich.logging import RichHandler

class Logging:

    def __initLogging__(self):
        self.log = logging.getLogger()
        self.console = Console()

        if eval(self.CONFIG["DEBUG"]):
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