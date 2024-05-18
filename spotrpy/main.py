import os
import sys
import argparse
import textwrap

from importlib import import_module
from .LOGO import SPOTR_LOGO


def main():
    """ Main """

    # Create parser
    parser      = create_parser()
    parsed_args = parser.parse_args()

    # Print info if no command was run
    if not parsed_args.command:
        print(textwrap.indent(SPOTR_LOGO, " " * 2))
        parser.print_help()
        sys.exit()

    # Initialize called command
    module          = import_module(f".commands.{parsed_args.command}", package="spotrpy")
    command_class   = getattr(module, parsed_args.command.capitalize())
    command         = command_class(parsed_args)
    
    #execute
    command.execute()

def create_parser():
    """ Create argument parser """

    parser = argparse.ArgumentParser(description="Spotr Command Line Interface")

    # Global options
    parser.add_argument("-d", "--debug", help="Run in debug mode", action="store_true")

    # Get all available commands
    commands = [file for file in os.listdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), "commands")) if file.endswith(".py")]
    commands = [file for file in commands if file not in ("__init__.py")]
    commands = [os.path.splitext(file)[0] for file in commands]
    
    # Add command info to subparser
    subparsers = parser.add_subparsers(dest='command', help='commands')

    for cmd in commands:
        module          = import_module(f".commands.{cmd}", package="spotrpy")
        command_class   = getattr(module, cmd.capitalize())
        cmd_parser      = subparsers.add_parser(cmd, help=command_class.description, description=command_class.description)

        command_class.add_arguments(cmd_parser)

    return parser

if __name__ == "__main__":
    main()