import questionary
from urllib.parse import urljoin, urlencode

class Playlist():
    """ Playlist class """

    def __init__(self, spotr):
        # Command info
        self.info = {
            'name': 'Playlist',
            'description': 'Choose a playlist',
            'arguments': [],
            'min_args': 0,
            'max_args': 0,
        }

        # Data URL
        self.URL = str(f"{urljoin(spotr.API_BASE_VERSION, 'me/playlists')}?{urlencode({'limit': spotr.SPOTIFY_LIMIT})}")

        # Arguments passed
        self.args = spotr.args

        # Unpack form spotr instance
        self.CONFIG = spotr.CONFIG
        self.request = spotr.request
        self.parse_items = spotr.parse_items
        self.play = spotr.play

    def execute(self):
        """Choose a playlist"""
        data = self.request("GET", self.URL)

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
        self.play(json=json)

