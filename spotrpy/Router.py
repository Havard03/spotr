""" Router Class """

import re
import os
import time
import webbrowser
import logging
import textwrap
import inspect
import questionary
from urllib.parse import urljoin, urlencode
from rich.console import Console
from tqdm import tqdm

from .ASCII import ASCII
from .API import API
from .Helpers import Helpers
from .Configuration import Configuration

log = logging.getLogger()
console = Console()

SPOTIFY_LIMIT = 50
QUSTIONARY_LIMIT = 36
API_BASE = "api.spotify.com"
API_VERSION = "v1"
API_PLAYER = urljoin("https://api.spotify.com", f"{API_VERSION}/me/player/")
API_BASE_VERSION = urljoin("https://api.spotify.com", f"{API_VERSION}/")

class Router(Configuration, API, Helpers, ASCII):
    """Available Spotr commands"""

    def refresh(self):
        """Refresh API key"""
        self.refresh_key()

    def next(self):
        """Play next track"""
        endpoint = urljoin(API_PLAYER, "next")
        self.request("POST", endpoint)
        self.current()

    def previous(self):
        """Play previous track"""
        endpoint = urljoin(API_PLAYER, "previous")
        self.request("POST", endpoint)
        self.current()

    def stop(self):
        """Stop/Pause playing"""
        endpoint = urljoin(API_PLAYER, "pause")
        self.request("PUT", endpoint)

    def start(self):
        """Start/Resume playing"""
        endpoint = urljoin(API_PLAYER, "play")
        self.request("PUT", endpoint)

    def play(self, json=None):
        """Play song or collection of songs"""
        self.request("PUT", str(urljoin(API_PLAYER, "play")), json=json)

    def replay(self):
        """Replay/Restart currently playing song"""
        self.request("PUT", str(f"{urljoin(API_PLAYER, "seek")}?{urlencode({"position_ms": 0})}"))
        self.current()

    def seek(self, progress):
        """Seek posistion for track in seconds"""
        self.request(
            "PUT",
            str(f"{urljoin(API_PLAYER, "seek")}?{urlencode({"position_ms": int(progress) * 1000})}")
        )

    def web(self):
        """Open currently playing track in a broswer"""
        data = self.request("GET", str(urljoin(API_PLAYER, "currently-playing")))
        if data is None:
            return
        webbrowser.open_new_tab(data["item"]["external_urls"]["spotify"])

    def shuffle(self):
        """Toggle shuffle, on / off"""
        state = questionary.select(
            "Choose playback state",
            choices=["true", "false"],
            erase_when_done=True,
            use_shortcuts=True,
        ).ask()
        self.request("PUT", str(f"{urljoin(API_PLAYER, "shuffle")}?{urlencode({"state": state})}"))

    def volume(self, volume=None):
        """Ajust volume"""
        if volume is None:
            volume = questionary.select(
                "Choose volume precentage",
                choices=["25%", "50%", "75%", "100%"],
                erase_when_done=True,
                use_shortcuts=True,
            ).ask()
        else:
            if int(volume) < 0:
                volume = 0
            elif int(volume) > 100:
                volume = 100
        self.request(
            "PUT",
            str(
                f"{urljoin(API_PLAYER, "volume")}?{urlencode({"volume_percent": str(volume).replace("%", "")})}"
            ),
        )
    vol = volume

    def playback(self):
        """Set playback state"""
        state = questionary.select(
            "Choose a play state",
            choices=["track", "context", "off"],
            erase_when_done=True,
            use_shortcuts=True,
        ).ask()
        if state is None:
            return
        self.request("PUT", str(f"{urljoin(API_PLAYER, "repeat")}?{urlencode({"state": state})}"))
        return

    def queue(self):
        """Get Queue"""
        data = self.request("GET", str(urljoin(API_PLAYER, "queue")))
        for track in data["queue"]:
            console.print(f"[bold green]{track['name']}")

    def recent(self):
        """Get recently played tracks"""
        data = self.request(
            "GET",
            str(f"{urljoin(API_PLAYER, "recently-played")}?{urlencode({"limit" : QUSTIONARY_LIMIT})}")
        )

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
        self.current()

    def playlist(self):
        """Choose a playlist"""
        data = self.request(
            "GET",
            str(
                f"{urljoin(API_BASE_VERSION, "me/playlists")}?{urlencode({"limit": SPOTIFY_LIMIT})}"
            )
        )

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
        self.current()
        return

    def playlistadd(self):
        """Add currently playing track to playlist"""

        data = self.request(
            "GET",
            str(f"{urljoin(API_BASE_VERSION, "me/playlists")}?{urlencode({"limit": SPOTIFY_LIMIT})}")
        )

        current_song = self.request("GET", str(urljoin(API_PLAYER, "currently-playing")))

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
            str(f"{urljoin(API_BASE_VERSION, f"playlists/{selected}/tracks")}?{urlencode({"uris": current_song["item"]["uri"]})}")
        )
        return

    def search(self, *query):
        """Search for anything on spotify, Types - track, playlist, album"""

        if not query:
            raise TypeError

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
                f"{urljoin(API_BASE_VERSION, "search")}?{urlencode({"q": " ".join(query), "type": search_type, "limit": QUSTIONARY_LIMIT})}"
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
        self.current()
        return

    def qsearch(self, *query):
        """Quicksearch for tracks"""
        if not query:
            raise TypeError

        data = self.request(
            "GET",
            str(
                f"{urljoin(API_BASE_VERSION, "search")}?{urlencode({"q": " ".join(query), "type": "track", "limit": 1})}"
            ),
        )

        json_id = [data['tracks']['items'][0]['uri']]
        json = {"uris": json_id, "offset": {"position": "0"}}
        self.play(json=json)
        self.current()
        return


    def recommend(self):
        """Play random / recommended tracks based on recent tracks"""
        recent = self.request(
            "GET", str(f"{urljoin(API_PLAYER, "recently-played")}?{urlencode({"limit": 5})}")
        )

        seed_arists = []
        seed_generes = ["all"]
        seed_tracks = []

        for track in recent["items"]:
            seed_tracks.append(track["track"]["id"])
            seed_arists.append(track["track"]["artists"][0]["id"])

        recommended = self.request(
            "GET",
            str(
                f"{urljoin(API_BASE_VERSION, "recommendations")}?{urlencode(
                    {
                        "seed_arists": ",".join(seed_arists),
                        "seed_generes": ",".join(seed_generes),
                        "seed_tracks": ",".join(seed_tracks),
                        "limit": 5,
                    }
                )}"
            ),
        )
        results = []
        for track in recommended["tracks"]:
            results.append(track["uri"])
        json = {"uris": results, "offset": {"position": "0"}}

        self.play(json=json)
        self.current()

    def ascii(self, width=None):
        """Ascii image for current track"""
        data = self.request("GET", str(urljoin(API_PLAYER, "currently-playing")))

        if width is None:
            width, height = os.get_terminal_size()

        ascii_str = (
            self.image_to_ascii_color(
                data["item"]["album"]["images"][0]["url"], int(width)
            )
            if eval(self.CONFIG["ASCII_IMAGE_COLOR"])
            else self.image_to_ascii(
                data["item"]["album"]["images"][0]["url"], int(width)
            )
        )
        lines = ascii_str.splitlines()
        for line in lines:
            print(line)

    def current(self):
        """Display information about the current track"""
        if inspect.stack()[1].filename == inspect.getfile(inspect.currentframe()):
            timeout = float(self.CONFIG["API_PROCESS_DELAY"])
            num_updates = int(timeout * 10)
            update_increment = 1 / 10  
            with tqdm(
                total=num_updates,
                desc="API Process Delay",
                unit="update",
                leave=True
            ) as pbar:
                for i in range(num_updates):
                    time.sleep(update_increment)
                    pbar.update(1)
            print("\033[F\033[K", end="")

        data = self.request("GET", str(urljoin(API_PLAYER, "currently-playing")))

        if data is None or data["item"] is None:
            log.error("No data")
            return

        if data["currently_playing_type"] not in ("track"):
            log.error("Playing unsupported type - %s", data['currently_playing_type'])
            return

        current_track = data["item"]
        album_data = current_track["album"]
        artist_names = ", ".join([artist["name"] for artist in current_track["artists"]])
        track_duration_ms = current_track["duration_ms"]
        track_duration_m, track_duration_s = divmod(track_duration_ms // 1000, 60)
        progress_ms = data["progress_ms"]
        progress_m, progress_s = divmod(progress_ms // 1000, 60)
        track_id = current_track["id"]
        track_name = current_track["name"]
        track_type = album_data["album_type"]
        album_name = album_data["name"]
        track_release_date = album_data["release_date"]
        track_url = current_track["external_urls"]["spotify"]
        track_image = album_data["images"][0]["url"]

        color_start = "\x1b[{}m".format
        color_end = "\x1b[0m"

        strings = textwrap.dedent(
            f"""
        {color_start('31')}Current track{color_end}
        {color_start('32')}------------------------------{color_end}
        {color_start('37')}Name{color_end}{color_start('32')}          -  {track_name}{color_end}
        {color_start('37')}Artits{color_end}{color_start('32')}        -  {artist_names}{color_end}
        {color_start('37')}Duration{color_end}{color_start('32')}      -  {track_duration_m} minutes {track_duration_s} seconds{color_end}
        {color_start('37')}Progress{color_end}{color_start('32')}      -  {progress_m} minutes {progress_s} seconds{color_end}
        {color_start('37')}Release date{color_end}{color_start('32')}  -  {track_release_date}{color_end}
        {color_start('37')}From{color_end}{color_start('32')}          -  {track_type} - {album_name}{color_end}
        {color_start('31')}Track details{color_end}
        {color_start('32')}------------------------------{color_end}
        {color_start('37')}Id{color_end}{color_start('32')}  - {track_id}{color_end}
        {color_start('37')}URL{color_end}{color_start('32')} - {track_url}{color_end}
        {color_start('37')}Image{color_end}{color_start('32')} - {track_image}{color_end}
        """
        )

        ansi_color_escape = re.compile(r"\x1b\[\d{1,2}m")
        strings_no_color = ansi_color_escape.sub("", strings)
        if not eval(self.CONFIG["ANSI_COLORS"]):
            strings = strings_no_color

        strings = strings.strip().splitlines()

        if eval(self.CONFIG["ASCII_IMAGE"]) or eval(self.CONFIG["USE_ASCII_LOGO"]):
            if eval(self.CONFIG["ASCII_IMAGE"]):
                width = self.CONFIG["ASCII_IMAGE_SIZE_WIDTH"]
                ascii_str = (
                    self.image_to_ascii_color(
                        data["item"]["album"]["images"][0]["url"], int(width)
                    )
                    if eval(self.CONFIG["ASCII_IMAGE_COLOR"])
                    else self.image_to_ascii(
                        data["item"]["album"]["images"][0]["url"], int(width)
                    )
                ).splitlines()
            elif eval(self.CONFIG["USE_ASCII_LOGO"]):
                ascii_str = self.CONFIG["ASCII_LOGO"]
            print()
            for i, line in enumerate(ascii_str):
                if eval(self.CONFIG["PRINT_DELAY_ACTIVE"]):
                    time.sleep(float(self.CONFIG["PRINT_DELAY"]))
                print(f"  {line}  {strings[i] if i < len(strings) else ''}")
            print()
        else:
            print()
            for line in strings:
                if eval(self.CONFIG["PRINT_DELAY_ACTIVE"]):
                    time.sleep(float(self.CONFIG["PRINT_DELAY"]))
                print(f"  {line}")
            print()
