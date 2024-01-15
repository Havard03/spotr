import questionary
from urllib.parse import urljoin, urlencode

class Recent():
    """ Recent class """

    def __init__(self, spotr):
        # Command info
        self.info = {
            'name': 'Recent',
            'description': 'Get recently played tracks',
            'arguments': [],
            'min_args': 0,
            'max_args': 0,
        }

        # Data URL
        self.URL = str(f"{urljoin(spotr.API_PLAYER, 'recently-played')}?{urlencode({'limit' : spotr.QUSTIONARY_LIMIT})}")

        # Arguments passed
        self.args = spotr.args

        # Unpack form spotr instance
        self.CONFIG = spotr.CONFIG
        self.request = spotr.request
        self.parse_items = spotr.parse_items
        self.play = spotr.play

    def execute(self):
        """Get recently played tracks"""
        data = self.request("GET", self.URL)

        choices = self.parse_items(
            data,
            accessor=["items"],
            return_value=["track", "uri"],
            name_value=["track", "name"],
            artists_value=["track", "artists"],
        )

        selected = questionary.select(
            "What song do you want to play?",
            choices=choices,
            erase_when_done=True,
            use_shortcuts=True,
            use_arrow_keys=True,
            use_jk_keys=False,
        ).ask()

        if selected is None:
            return

        json_data = {"uris": [selected]}
        self.play(json=json_data)


