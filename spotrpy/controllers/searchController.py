import questionary
from urllib.parse import urljoin, urlencode

from spotrpy.core.BaseController import BaseController
from spotrpy.util.Helpers import Helpers


class searchController(BaseController, Helpers):

    def run(self):
        search_types = {
            "track": {
                "accessor": ["tracks", "items"],
                "return_value": ["uri"],
                "name_value": ["name"],
                "artists_value": ["artists"],
                "artists_array": True,
                "json_value": "uris",
                "json_value_array": True,
                "json": {"uris": []},
            },
            "playlist": {
                "accessor": ["playlists", "items"],
                "return_value": ["uri"],
                "name_value": ["name"],
                "artists_value": ["owner", "display_name"],
                "artists_array": False,
                "json_value": "context_uri",
                "json_value_array": False,
                "json": {"context_uri": [], "offset": {"position": "0"}},
            },
            "album": {
                "accessor": ["albums", "items"],
                "return_value": ["uri"],
                "name_value": ["name"],
                "artists_value": ["artists"],
                "artists_array": True,
                "json_value": "context_uri",
                "json_value_array": False,
                "json": {"context_uri": [], "offset": {"position": "0"}},
            },
        }

        if not self.args.type:
            available_types = ["track", "playlist", "album"]
            search_type = questionary.select(
                "Select search type",
                choices=available_types,
                erase_when_done=True,
                use_shortcuts=True,
                use_arrow_keys=True,
                use_jk_keys=False,
            ).ask()
            if search_type is None:
                return
        else:
            search_type = self.args.type

        self.fetch(search_type)

        choices = self.parse_items(
            self.response,
            accessor=search_types[search_type]["accessor"],
            return_value=search_types[search_type]["return_value"],
            name_value=search_types[search_type]["name_value"],
            artists_value=search_types[search_type]["artists_value"],
            artists_array=search_types[search_type]["artists_array"],
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

        json = search_types[search_type]["json"]
        if search_types[search_type]["json_value_array"]:
            json[search_types[search_type]["json_value"]] = [selected]
        else:
            json[search_types[search_type]["json_value"]] = selected

        self.request("PUT", str(urljoin(self.API_PLAYER, "play")), json=json)

    def fetch(self, search_type):
        self.response = self.request(
            "GET",
            str(
                f"{urljoin(self.API_BASE_VERSION, 'search')}?{urlencode({'q': ' '.join(self.args.query), 'type': search_type, 'limit': self.QUSTIONARY_LIMIT})}"
            )
        )


