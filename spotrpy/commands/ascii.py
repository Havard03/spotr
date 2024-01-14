import os
from urllib.parse import urljoin

class Ascii():
    """ Ascii class """

    def __init__(self, spotr):
        # Command info
        self.info = {
            'name': 'Ascii',
            'description': 'Ascii image for current track',
            'arguments': ['Width(optional)'],
            'min_args': 0,
            'max_args': 1,
        }

        # Data URL
        self.URL = str(urljoin(spotr.API_PLAYER, "currently-playing"))

        # Arguments passed
        self.args = spotr.args

        # Unpack needed form spotr instance
        self.CONFIG = spotr.CONFIG
        self.request = spotr.request
        self.log = spotr.log
        self.image_to_ascii = spotr.image_to_ascii
        self.image_to_ascii_color = spotr.image_to_ascii_color    

    def execute(self, width=None):
        """Ascii image for current track"""
        data = self.request("GET", self.URL)

        if data is None or data["item"] is None:
            self.log.error("No data")
            return
        
        if width is None:
            width, height = os.get_terminal_size()

        ascii_str = (
            self.image_to_ascii_color(
                data["item"]["album"]["images"][0]["url"], int(width)
            )
            if eval(self.CONFIG["ASCII_IMAGE_COLOR"])
            else self.image_to_ascii(
                data["item"]["album"]["images"][0]["url"], int(width)
            )
        )
        lines = ascii_str.splitlines()
        for line in lines:
            print(line)

