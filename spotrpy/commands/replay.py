from ..spotr import Spotr
from urllib.parse import urljoin, urlencode

class Replay(Spotr):
    """ Replay """

    description = "Replay/Restart currently playing track"

    def __init__(self, args):
        self.args = args
        Spotr.__init__(self)

    @staticmethod
    def add_arguments(parser):
        pass

    def execute(self):
        self.request("PUT", f"{urljoin(self.API_PLAYER, 'seek')}?{urlencode({'position_ms': 0})}")
