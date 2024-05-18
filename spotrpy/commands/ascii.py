import os

from ..spotr import Spotr
from urllib.parse import urljoin

class Ascii(Spotr):
    """ Ascii """

    description = "Ascii image for current track"

    def __init__(self, args):
        self.args = args
        Spotr.__init__(self)

    @staticmethod
    def add_arguments(parser):
        parser.add_argument(
            '-w', '--width', type=str, help="Set ascii image width"
        ) 

    def execute(self):
        data = self.request("GET", urljoin(self.API_PLAYER, "currently-playing"))

        if data is None or data["item"] is None:
            self.log.error("No data")
            return
        
        if self.args.width is None:
            width, height = os.get_terminal_size()
        else:
            width = self.args.width

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

