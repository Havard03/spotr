""" Helper Class """

import re

from rich.console import Console

console = Console()

class Helpers:
    """Helper functions for Router"""

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
        available_functions = [
            x for x in dir(self) if x not in self.CONFIG["IGNORED_FUNCTIONS"]
        ]
        longest_function = max(available_functions, key=len)

        available_functions.insert(0, "[bold red]ARGUMENTS[/bold red]")
        available_functions.insert(1, "---------------------------------------")

        if eval(self.CONFIG["USE_ASCII_LOGO"]):
            ASCII_LOGO = self.CONFIG["ASCII_LOGO"].splitlines()
            seperator_length = max(ASCII_LOGO, key=len)
            print()
            for i, function in enumerate(available_functions):
                ascii_part = ASCII_LOGO[i] if i < len(ASCII_LOGO) else ""
                function_part = f"{function:<{len(longest_function)}}"

                if i > 1:
                    docstring = getattr(self, function).__doc__
                    format_string = f"[bold green]  {ascii_part.ljust(len(seperator_length))}   [bold white]{function_part}[/bold white] - {docstring}"
                else:
                    format_string = f"[bold green]  {ascii_part.ljust(len(seperator_length))}   {function}"

                console.print(
                    format_string
                    if eval(self.CONFIG["ANSI_COLORS"])
                    else re.sub(r"\[.*?\]", "", format_string)
                )
            print()
        else:
            print()
            for i, function in enumerate(available_functions):
                function_part = f"{function:<{len(longest_function)}}"
                if i > 1:
                    docstring = getattr(self, function).__doc__
                    format_string = f"[bold green] [bold white]{function_part}[/bold white] - {docstring}"
                else:
                    format_string = f"[bold green] {function}"

                console.print(
                    format_string
                    if eval(self.CONFIG["ANSI_COLORS"])
                    else re.sub(r"\[.*?\]", "", format_string)
                )
            print()
