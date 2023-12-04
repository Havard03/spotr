# Importing necessary modules
import re
from rich.console import Console

# Creating a Console instance for rich text formatting
console = Console()


class Helpers:
    """Helper functions for Router"""

    def get_item(self, data, keys):
        """Navigates through nested dictionaries/lists to access specific data."""
        # Iteratively access nested data using keys
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
        """Formats data into a structured list of choices for display or selection."""
        # Initialize variables
        choices = []
        track_width = 0

        # Calculating the maximum width for track names, if artists are included
        if artists_value:
            names = [
                self.get_item(item, name_value)
                for item in self.get_item(data, accessor)
            ]
            if names:
                track_width = max(map(len, names))

        # Iterating through items and formatting them for display
        for item in self.get_item(data, accessor):
            track_name = self.get_item(item, name_value)
            if artists_value:
                # Formatting artist names based on whether it's a single value or an array
                if artists_array:
                    artist_names = ", ".join(
                        artist["name"]
                        for artist in (self.get_item(item, artists_value))
                    )
                else:
                    artist_names = self.get_item(item, artists_value)
                # Appending formatted track and artist names to choices
                choices.append(
                    {
                        "name": "{0:<{track_width}} -- {1}".format(
                            track_name, artist_names, track_width=track_width
                        ),
                        "value": self.get_item(item, return_value),
                    }
                )
            else:
                # Appending track names to choices when artist info is not included
                choices.append(
                    {
                        "name": track_name,
                        "value": self.get_item(item, return_value),
                    }
                )
        return choices

    def parse_functions(self):
        """Displays a list of available functions/commands."""
        # Getting a list of available functions excluding those in IGNORED_FUNCTIONS
        available_functions = [
            x for x in dir(self) if x not in self.CONFIG["IGNORED_FUNCTIONS"]
        ]
        longest_function = max(available_functions, key=len)

        # Preparing headers for the display
        available_functions.insert(0, "[bold red]ARGUMENTS[/bold red]")
        available_functions.insert(1, "---------------------------------------")

        # Display ASCII logo if configured
        if eval(self.CONFIG["USE_ASCII_LOGO"]):
            ASCII_LOGO = self.CONFIG["ASCII_LOGO"].splitlines()
            seperator_length = max(ASCII_LOGO, key=len)
            print()
            for i, function in enumerate(available_functions):
                ascii_part = ASCII_LOGO[i] if i < len(ASCII_LOGO) else ""
                function_part = f"{function:<{len(longest_function)}}"
                docstring = getattr(self, function).__doc__ if i > 1 else ""
                format_string = self._prepare_format_string(
                    ascii_part, seperator_length, function_part, docstring
                )
                console.print(format_string)
            print()
        else:
            # Display without ASCII logo
            print()
            for i, function in enumerate(available_functions):
                function_part = f"{function:<{len(longest_function)}}"
                docstring = getattr(self, function).__doc__ if i > 1 else ""
                format_string = self._prepare_format_string(
                    "", 0, function_part, docstring
                )
                console.print(format_string)
            print()

    def _prepare_format_string(
        self, ascii_part, seperator_length, function_part, docstring
    ):
        """Helper method to prepare the format string for displaying function info."""
        if ascii_part:
            ascii_formatted = f"{ascii_part.ljust(len(seperator_length))}"
            format_string = f"[bold green]  {ascii_formatted}   [bold white]{function_part}[/bold white] - {docstring}"
        else:
            format_string = (
                f"[bold green] [bold white]{function_part}[/bold white] - {docstring}"
            )
        # Removing ANSI color codes if not configured to use ANSI colors
        return (
            format_string
            if eval(self.CONFIG["ANSI_COLORS"])
            else re.sub(r"\[.*?\]", "", format_string)
        )
