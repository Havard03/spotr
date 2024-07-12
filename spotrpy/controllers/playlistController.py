import questionary

from urllib.parse import urljoin, urlencode

from spotrpy.core.BaseController import BaseController
from spotrpy.util.Helpers import Helpers


class playlistController(BaseController, Helpers):

    def run(self):
        self.fetch()

        choices = self.parse_items(
            self.response,
            accessor=["items"],
            return_value=["uri"],
            name_value=["name"],
            artists_value=False,
        )

        selected = questionary.select(
            "What playlist do you want to play?",
            choices=choices,
            erase_when_done=True,
            use_arrow_keys=True,
            use_jk_keys=False,
        ).ask()
        if selected is None:
            return

        json = {"context_uri": selected, "offset": {"position": "0"}}
        self.request("PUT", str(urljoin(self.API_PLAYER, "play")), json=json)

    def fetch(self):
        self.response = self.request("GET", f"{urljoin(self.API_BASE_VERSION, 'me/playlists')}?{urlencode({'limit': self.SPOTIFY_LIMIT})}")
