import questionary
from urllib.parse import urljoin, urlencode

class Search():
    """ Search class """

    def __init__(self, spotr):
        # Command info
        self.info = {
            'name': 'Search',
            'description': 'Search for anything on spotify, Types - track, playlist, album',
            'arguments': [['Query...'],['Type', 'Query...']],
            'min_args': 1,
            'max_args': 999,
        }

        # Arguments passed
        self.args = spotr.args

        # Unpack form spotr instance
        self.CONFIG = spotr.CONFIG
        self.request = spotr.request
        self.play = spotr.play
        self.parse_items = spotr.parse_items
        self.API_BASE_VERSION = spotr.API_BASE_VERSION
        self.QUSTIONARY_LIMIT = spotr.QUSTIONARY_LIMIT


    def execute(self, *query):
        """Search for anything on spotify, Types - track, playlist, album"""
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

        if query[0] not in ["track", "playlist", "album"]:
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
            query = list(query)
            search_type = query[0]
            query.pop(0)

        data = self.request(
            "GET",
            str(
                f"{urljoin(self.API_BASE_VERSION, 'search')}?{urlencode({'q': ' '.join(query), 'type': search_type, 'limit': self.QUSTIONARY_LIMIT})}"
            )
        )

        choices = self.parse_items(
            data,
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

        self.play(json=json)



