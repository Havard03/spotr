from ..spotr import Spotr
from urllib.parse import urljoin, urlencode

class Recommend(Spotr):
    """ Recommend """

    description = "Play random / recommended tracks based on recent tracks"

    def __init__(self, args):
        self.args = args
        Spotr.__init__(self)

    @staticmethod
    def add_arguments(parser):
        pass

    def execute(self):
        recent = self.request(
            "GET", f"{urljoin(self.API_PLAYER, 'recently-played')}?{urlencode({'limit': 5})}"
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
        self.request("PUT", str(urljoin(self.API_PLAYER, "play")), json=json)
