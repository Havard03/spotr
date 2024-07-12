
from urllib.parse import urljoin, urlencode

from spotrpy.core.BaseController import BaseController


class replayController(BaseController):

    def run(self):
        self.request("PUT", f"{urljoin(self.API_PLAYER, 'seek')}?{urlencode({'position_ms': 0})}")
