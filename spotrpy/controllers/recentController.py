import questionary
from urllib.parse import urljoin, urlencode

from spotrpy.core.BaseController import BaseController
from spotrpy.util.Helpers import Helpers


class recentController(BaseController, Helpers):

    def run(self):
        self.fetch()

        choices = self.parse_items(
            self.response,
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

    def fetch(self):
        self.response = self.request("GET", f"{urljoin(self.API_PLAYER, 'recently-played')}?{urlencode({'limit' : self.QUSTIONARY_LIMIT})}")
