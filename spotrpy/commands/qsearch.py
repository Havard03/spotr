from ..spotr import Spotr
from urllib.parse import urljoin, urlencode

class Qsearch(Spotr):
    """ Qsearch """

    description = "Quicksearch for tracks"

    def __init__(self, args):
        self.args = args
        Spotr.__init__(self)

    @staticmethod
    def add_arguments(parser):
        parser.add_argument(
            'query', type=str, help="Search query", nargs='*'
        )

    def execute(self):
        data = self.request(
            "GET",
            str(
                f"{urljoin(self.API_BASE_VERSION, 'search')}?{urlencode({'q': ' '.join(self.args.query), 'type': 'track', 'limit': 1})}"
            ),
        )
        json_id = [data['tracks']['items'][0]['uri']]
        json = {"uris": json_id, "offset": {"position": "0"}}

        self.request("PUT", str(urljoin(self.API_PLAYER, "play")), json=json)
