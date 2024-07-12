import argparse
import textwrap
import inspect

from spotrpy.commands import Command 
from spotrpy.assets.LOGO import SPOTR_LOGO

from spotrpy.logging.Logging import Logging

"""
    Initializes ArgumentParser and parses commands from commands.py then runs given method
"""

class Parser(Logging):
    """ Parser """

    def __init__(self) -> None:
        """ Overview of entire command execution """

        self.parser = argparse.ArgumentParser(description="Spotr Command Line Interface")
        self.args()
        self.subParsers()
        
        super().__initLogging__(self.parsed_args)
        self.log.debug(self.parsed_args)

        self.exec()
        self.postExec()

    def args(self) -> None:
        """ Universal arguments  """

        self.parser.add_argument("-d", "--debug", help="Run in debug", action="store_true")
        self.parser.add_argument("-c", "--current", help="Run current, post exec", action="store_true")

    def subParsers(self) -> None:
        """ Parse defined commands and add to ArgumentParser """

        subparser = self.parser.add_subparsers(dest='command')

        for command in Command.commands:
            command_parser = subparser.add_parser(
                Command.commands[command]['name'], 
                help=Command.commands[command]['desc'],
                description=Command.commands[command]['desc']
            )

            if Command.commands[command]['options']:
                for option in Command.commands[command]['options']:
                    command_parser.add_argument(
                        *option['flags'],
                        **option['kwargs']
                    )

        self.parsed_args = self.parser.parse_args()

    def exec(self, command=None) -> None:
        """ Command execution logic """

        if command is None: command = self.parsed_args.command

        if self.parsed_args.command:
            self.log.debug(f"Executing {Command.commands[command]['callable']}")
            
            callable = Command.commands[command]['callable']

            if isinstance(callable, list):
                controller = callable[0](self.parsed_args)
                getattr(controller, callable[1])()
            elif inspect.isfunction(callable):
                Command.commands[command]['callable'](self.parsed_args)
            else:
                self.log.error("Callable must be of type class or function")
        else:
            print(textwrap.indent(SPOTR_LOGO, " " * 2))
            self.parser.print_help()

    def postExec(self) -> None:
        """ Post execution logic """

        if self.parsed_args.current: self.exec("current")


