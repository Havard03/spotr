from urllib.parse import urljoin

from spotrpy.core.BaseController import BaseController


class nextController(BaseController):

    def run(self):
        self.request("POST", urljoin(self.API_PLAYER, "next"))
