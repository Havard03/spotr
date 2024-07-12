from urllib.parse import urljoin

from spotrpy.core.BaseController import BaseController

class previousController(BaseController):

    def run(self):
        self.request("POST", urljoin(self.API_PLAYER, "previous"))
