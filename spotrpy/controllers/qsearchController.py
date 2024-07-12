
from urllib.parse import urljoin, urlencode

from spotrpy.core.BaseController import BaseController


class qsearchController(BaseController):

    def run(self):
        self.fetch()
        json_id = [self.response['tracks']['items'][0]['uri']]
        json = {"uris": json_id, "offset": {"position": "0"}}

        self.request("PUT", str(urljoin(self.API_PLAYER, "play")), json=json)

    def fetch(self):
        self.response = self.request(
            "GET",
            str(
                f"{urljoin(self.API_BASE_VERSION, 'search')}?{urlencode({'q': ' '.join(self.args.query), 'type': 'track', 'limit': 1})}"
            ),
        )
