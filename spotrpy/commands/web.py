import webbrowser

from ..spotr import Spotr
from urllib.parse import urljoin

class Web(Spotr):
    """ Web """

    description = "Open currently playing track in a broswer"

    def __init__(self, args):
        self.args = args
        Spotr.__init__(self)

    @staticmethod
    def add_arguments(parser):
        pass

    def execute(self):
        data = self.request("GET", urljoin(self.API_PLAYER, "currently-playing"))
        if data is None: return
        webbrowser.open_new_tab(data["item"]["external_urls"]["spotify"])
