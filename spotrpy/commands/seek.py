from ..spotr import Spotr
from urllib.parse import urljoin, urlencode

class Seek(Spotr):
    """ Seek """

    description = "Seek posistion for track (in seconds)"

    def __init__(self, args):
        self.args = args
        Spotr.__init__(self)

    @staticmethod
    def add_arguments(parser):
        parser.add_argument(
            'seconds', type=str, help="Song posistion"
        )

    def execute(self):
        self.request(
            "PUT",
            str(f"{urljoin(self.API_PLAYER, 'seek')}?{urlencode({'position_ms': int(self.args.seconds) * 1000})}")
        )
