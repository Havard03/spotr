""" Helper Class """
import os
import sys
import textwrap

class Helpers:
    """Helper functions"""

    def get_item(self, data, keys):
        """Access data with accessor"""
        for key in keys:
            data = data[key]
        return data

    def parse_items(
        self,
        data,
        accessor,
        return_value,
        name_value,
        artists_value=False,
        artists_array=True,
    ):
        """Parse tracks for questionary"""
        choices = []
        track_width = 0

        if artists_value:
            names = [
                self.get_item(item, name_value)
                for item in self.get_item(data, accessor)
            ]
            if names:
                track_width = max(map(len, names))

        for item in self.get_item(data, accessor):
            track_name = self.get_item(item, name_value)
            if artists_value:
                if artists_array:
                    artist_names = ", ".join(
                        artist["name"]
                        for artist in (self.get_item(item, artists_value))
                    )
                else:
                    artist_names = self.get_item(item, artists_value)
                choices.append(
                    {
                        "name": "{0:<{track_width}} -- {1}".format(
                            track_name, artist_names, track_width=track_width
                        ),
                        "value": self.get_item(item, return_value),
                    }
                )
            else:
                choices.append(
                    {
                        "name": track_name,
                        "value": self.get_item(item, return_value),
                    }
                )
        return choices

    def parse_functions(self):
        """Parse and display available funcions / commands"""
        if eval(self.CONFIG["ANSI_COLORS"]):
            self.console.print(f"[bold green]{textwrap.indent(self.CONFIG['ASCII_LOGO'], '  ')}")
            self.console.print("  [bold red]Avaiable commands[/bold red]")
            self.console.print("  [bold green]---------------------------------------")
        else:
            self.console.print(self.CONFIG["ASCII_LOGO"])
            print("  Avaiable commands")
            print("  ---------------------------------------")

        commands = [file for file in os.listdir(os.path.join(self.CONFIG["path"], "../commands")) if file.endswith(".py")]
        commands = [file for file in commands if file != "__init__.py"]
        commands = [os.path.splitext(file)[0] for file in commands]

        for i in range(0, len(commands), 5):
            group = commands[i:i+5]
            if eval(self.CONFIG["ANSI_COLORS"]):
                self.console.print(f"  [bold white]{', '.join(group)}")
            else:
                self.console.print(f"  {group}")
        print()
        if eval(self.CONFIG["ANSI_COLORS"]):
            self.console.print("  [bold blue]Info[/bold blue]")
            self.console.print("  [bold green]---------------------------------------")
            self.console.print("  [bold white]For info on commands, help followed by command.")
            self.console.print("  [bold white]Spotr help <command>.")
        else:
            self.console.print(self.CONFIG["ASCII_LOGO"])
            print("  Info")
            print("  ---------------------------------------")
            print("  [bold white]For info on commands, help followed by command.")
            print("  [bold white]Spotr help <command>.")
        print()

    def commandArgs(self, info, args):
        """ Check if the number of arguments is within the expected range """
        if not (info['min_args'] <= len(args) <= info['max_args']):
            self.log.info(f"Invalid number of arguments. Expected: {info['arguments']}")
            self.commandInfo(info)
            sys.exit(1)

    def commandInfo(self, info):
        """ Print information about the command and its arguments """
        self.log.info(textwrap.dedent(f"""
            Command: {info['name']}
            Description: {info['description']}
            Expected Arguments: {info['arguments']}
            Minimum Arguments: {info['min_args']}
            Maximum Arguments: {info['max_args']}
        """))


        