from urllib.parse import urljoin, urlencode

class Recommend():
    """ Recommend class """

    def __init__(self, spotr):
        # Command info
        self.info = {
            'name': 'Recommend',
            'description': 'Play random / recommended tracks based on recent tracks',
            'arguments': [],
            'min_args': 0,
            'max_args': 0,
        }

        # Data URL
        self.URL = str(f"{urljoin(spotr.API_PLAYER, 'recently-played')}?{urlencode({'limit': 5})}")

        # Arguments passed
        self.args = spotr.args

        # Unpack form spotr instance
        self.CONFIG = spotr.CONFIG
        self.request = spotr.request
        self.play = spotr.play
        self.API_BASE_VERSION = spotr.API_BASE_VERSION

    def execute(self):
        """Play random / recommended tracks based on recent tracks"""
        recent = self.request(
            "GET", self.URL
        )

        seed_arists = []
        seed_generes = ["all"]
        seed_tracks = []

        for track in recent["items"]:
            seed_tracks.append(track["track"]["id"])
            seed_arists.append(track["track"]["artists"][0]["id"])

        recommended = self.request(
            "GET",
            str(
                f"{urljoin(self.API_BASE_VERSION, 'recommendations')}?{urlencode(
                    {
                        'seed_arists': ','.join(seed_arists),
                        'seed_generes': ','.join(seed_generes),
                        'seed_tracks': ','.join(seed_tracks),
                        'limit': 5,
                    }
                )}"
            ),
        )
        results = []
        for track in recommended["tracks"]:
            results.append(track["uri"])
        json = {"uris": results, "offset": {"position": "0"}}

        self.play(json=json)
        self.current()
