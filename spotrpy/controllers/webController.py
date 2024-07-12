import webbrowser
from urllib.parse import urljoin

from spotrpy.core.BaseController import BaseController

class webController(BaseController):

    def run(self):
        data = self.request("GET", urljoin(self.API_PLAYER, "currently-playing"))
        if data is None: return
        webbrowser.open_new_tab(data["item"]["external_urls"]["spotify"])
