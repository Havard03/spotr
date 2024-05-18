import questionary

from ..spotr import Spotr
from urllib.parse import urljoin, urlencode

class Volume(Spotr):
    """ Volume """

    description = "Ajust volume"

    def __init__(self, args):
        self.args = args
        Spotr.__init__(self)

    @staticmethod
    def add_arguments(parser):
        parser.add_argument(
            '-p', '--percentage', type=str, help="Volume percentage"
        )

    def execute(self):
        if self.args.percentage is None:
            volume = questionary.select(
                "Choose volume precentage",
                choices=["25%", "50%", "75%", "100%"],
                erase_when_done=True,
                use_shortcuts=True,
            ).ask()
        else:
            volume = self.args.percentage

        self.request(
            "PUT",
            str(
                f"{urljoin(self.API_PLAYER, 'volume')}?{urlencode({'volume_percent': str(volume).replace('%', '')})}"
            ),
        )
