from ..spotr import Spotr
from urllib.parse import urljoin

class Stop(Spotr):
    """ Stop """

    description = "Stop/Pause playing"

    def __init__(self, args):
        self.args = args
        Spotr.__init__(self)

    @staticmethod
    def add_arguments(parser):
        pass

    def execute(self):
        self.request("PUT", urljoin(self.API_PLAYER, "pause"))
