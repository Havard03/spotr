from urllib.parse import urljoin, urlencode

from spotrpy.core.BaseController import BaseController


class recommendController(BaseController):

    def run(self):
        self.fetch()
        
        seed_arists = []
        seed_generes = ["all"]
        seed_tracks = []

        for track in self.response["items"]:
            seed_tracks.append(track["track"]["id"])
            seed_arists.append(track["track"]["artists"][0]["id"])
            
        params = urlencode(
            {
                'seed_arists': ','.join(seed_arists),
                'seed_generes': ','.join(seed_generes),
                'seed_tracks': ','.join(seed_tracks),
                'limit': 5,
            }
        )

        recommended = self.request(
            "GET",
            str(
                f"{urljoin(self.API_BASE_VERSION, 'recommendations')}?{params}"
            ),
        )
        results = []
        for track in recommended["tracks"]:
            results.append(track["uri"])
        json = {"uris": results, "offset": {"position": "0"}}

        self.request("PUT", str(urljoin(self.API_PLAYER, "play")), json=json)

    def fetch(self):
        self.response = self.request(
            "GET", f"{urljoin(self.API_PLAYER, 'recently-played')}?{urlencode({'limit': 5})}"
        )
