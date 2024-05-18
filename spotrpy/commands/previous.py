from ..spotr import Spotr
from urllib.parse import urljoin

class Previous(Spotr):
    """ Previous """

    description = "Play previous track"

    def __init__(self, args):
        self.args = args
        Spotr.__init__(self)

    @staticmethod
    def add_arguments(parser):
        pass

    def execute(self):
        self.request("POST", urljoin(self.API_PLAYER, "previous"))
