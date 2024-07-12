
from urllib.parse import urljoin, urlencode

from spotrpy.core.BaseController import BaseController


class seekController(BaseController):

    def run(self):
        self.request(
            "PUT",
            str(f"{urljoin(self.API_PLAYER, 'seek')}?{urlencode({'position_ms': int(self.args.seconds) * 1000})}")
        )
