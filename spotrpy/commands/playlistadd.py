import questionary

from ..spotr import Spotr
from urllib.parse import urljoin, urlencode

class Playlistadd(Spotr):
    """ Playlistadd """

    description = "Add currently playing track to a playlist"

    def __init__(self, args):
        self.args = args
        Spotr.__init__(self)

    @staticmethod
    def add_arguments(parser):
        pass

    def execute(self):
        data = self.request("GET", f"{urljoin(self.API_BASE_VERSION, 'me/playlists')}?{urlencode({'limit': self.SPOTIFY_LIMIT})}")
        current_song = self.request("GET", urljoin(self.API_PLAYER, "currently-playing"))

        choices = self.parse_items(
            data,
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
            str(f"{urljoin(self.API_BASE_VERSION, f"playlists/{selected}/tracks")}?{urlencode({"uris": current_song["item"]["uri"]})}")
        )