from ..spotr import Spotr
from urllib.parse import urljoin, urlencode

class Queue(Spotr):
    """ Queue """

    description = "Display current queue"

    def __init__(self, args):
        self.args = args
        Spotr.__init__(self)

    @staticmethod
    def add_arguments(parser):
        pass

    def execute(self):
        data = self.request("GET", urljoin(self.API_PLAYER, "queue"))

        for track in data["queue"]:
            self.console.print(f"[bold green]{track['name']}")
