import questionary
from urllib.parse import urljoin, urlencode

class Playlistadd():
    """ Playlistadd class """

    def __init__(self, spotr):
        # Command info
        self.info = {
            'name': 'PlaylistAdd',
            'description': 'Add currently playing track to playlist',
            'arguments': [],
            'min_args': 0,
            'max_args': 0,
        }

        # Data URL
        self.DATA_URL = str(f"{urljoin(spotr.API_BASE_VERSION, 'me/playlists')}?{urlencode({'limit': spotr.SPOTIFY_LIMIT})}")
        self.CURRENT_URL = str(urljoin(spotr.API_PLAYER, "currently-playing"))

        # Arguments passed
        self.args = spotr.args

        # Unpack form spotr instance
        self.CONFIG = spotr.CONFIG
        self.request = spotr.request
        self.parse_items = spotr.parse_items
        self.API_BASE_VERSION = spotr.API_BASE_VERSION

    def execute(self):
        """Add currently playing track to playlist"""
        data = self.request("GET", self.DATA_URL)
        current_song = self.request("GET", self.CURRENT_URL)

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

