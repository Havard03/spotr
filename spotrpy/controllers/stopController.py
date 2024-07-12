
from urllib.parse import urljoin

from spotrpy.core.BaseController import BaseController


class stopController(BaseController):

    def run(self):
        self.request("PUT", urljoin(self.API_PLAYER, "pause"))
