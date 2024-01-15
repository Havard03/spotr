from urllib.parse import urljoin, urlencode

class Qsearch():
    """ Qsearch class """

    def __init__(self, spotr):
        # Command info
        self.info = {
            'name': 'Qsearch (Quicksearch)',
            'description': 'Quicksearch for tracks',
            'arguments': ['Query...'],
            'min_args': 1,
            'max_args': 999,
        }

        # Arguments passed
        self.args = spotr.args

        # Unpack form spotr instance
        self.CONFIG = spotr.CONFIG
        self.request = spotr.request
        self.play = spotr.play
        self.API_BASE_VERSION = spotr.API_BASE_VERSION


    def execute(self, *query):
        """ Info """
        data = self.request(
            "GET",
            str(
                f"{urljoin(self.API_BASE_VERSION, 'search')}?{urlencode({'q': ' '.join(query), 'type': 'track', 'limit': 1})}"
            ),
        )

        json_id = [data['tracks']['items'][0]['uri']]
        json = {"uris": json_id, "offset": {"position": "0"}}
        self.play(json=json)
