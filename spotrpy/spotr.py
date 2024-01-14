import sys
from importlib import import_module

from .Util.API import API
from .Util.ASCII import ASCII
from .Util.Helpers import Helpers
from .Util.Configuration import Configuration
from .Util.Logging import Logging

class Spotr(
    Configuration, 
    Logging, 
    API, 
    ASCII, 
    Helpers,
):
    """Spotr"""
    def __init__(self, args):
        super().__initConfig__()
        super().__initLogging__()
        super().__initAPI__()
        self.args = args

    def run(self):
        """Run spotr command"""
        if not self.args:
            self.parse_functions()
            exit()
        try:
            if self.args[0].lower() in ["help", "info"]:
                module = import_module(f".commands.{self.args[1]}", package="spotrpy")
                command = getattr(module, f"{self.args[1].capitalize()}")(self)
                self.commandInfo(command.info)
            else:
                module = import_module(f".commands.{self.args[0]}", package="spotrpy")
                command = getattr(module, f"{self.args[0].capitalize()}")(self)
                self.commandArgs(command.info, command.args[1:])
                command.execute(*command.args[1:])
        except ModuleNotFoundError as e:
            self.log.exception(f"Unknown command: {e}")
            sys.exit(1)

def main():
    """main"""
    spotr = Spotr(sys.argv[1:])
    spotr.run()

if __name__ == "__main__":
    main()