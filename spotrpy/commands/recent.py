import questionary

from ..spotr import Spotr
from urllib.parse import urljoin, urlencode

class Recent(Spotr):
    """ Recent """

    description = "Select one of recently played tracks"

    def __init__(self, args):
        self.args = args
        Spotr.__init__(self)

    @staticmethod
    def add_arguments(parser):
        pass

    def execute(self):
        data = self.request("GET", f"{urljoin(self.API_PLAYER, 'recently-played')}?{urlencode({'limit' : self.QUSTIONARY_LIMIT})}")

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

        json = {"uris": [selected]}
        self.request("PUT", str(urljoin(self.API_PLAYER, "play")), json=json)