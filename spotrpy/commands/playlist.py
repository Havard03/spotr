import questionary

from ..spotr import Spotr
from urllib.parse import urljoin, urlencode

class Playlist(Spotr):
    """ Playlist """

    description = "Start playing one of your playlists"

    def __init__(self, args):
        self.args = args
        Spotr.__init__(self)

    @staticmethod
    def add_arguments(parser):
        pass

    def execute(self):
        data = self.request("GET", f"{urljoin(self.API_BASE_VERSION, 'me/playlists')}?{urlencode({'limit': self.SPOTIFY_LIMIT})}")

        choices = self.parse_items(
            data,
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
