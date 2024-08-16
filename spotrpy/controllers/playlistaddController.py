import questionary
from urllib.parse import urljoin, urlencode

from spotrpy.core.BaseController import BaseController
from spotrpy.util.Helpers import Helpers


class playlistaddController(BaseController, Helpers):

    def run(self):
        self.fetch()
        choices = self.parse_items(
            self.response,
            accessor=["items"],
            return_value=["id"],
            name_value=["name"],
            artists_value=False,
        )

        selected = questionary.select(
            "what playlist do you want to add track to?",
            choices=choices,
            erase_when_done=True,
            use_arrow_keys=True,
            use_jk_keys=False,
        ).ask()

        if selected is None:
            return

        self.request(
            "POST",
            str(f'{urljoin(self.API_BASE_VERSION, f"playlists/{selected}/tracks")}?{urlencode({"uris": self.current_song["item"]["uri"]})}')
        )

    def fetch(self):
        self.response = self.request("GET", f"{urljoin(self.API_BASE_VERSION, 'me/playlists')}?{urlencode({'limit': self.SPOTIFY_LIMIT})}")
        self.current_song = self.request("GET", urljoin(self.API_PLAYER, "currently-playing"))

