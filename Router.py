""" Router Class """

import re
import time
import webbrowser
import logging
import textwrap
import inspect
import questionary
from rich.console import Console
from urllib.parse import urljoin
from tqdm import tqdm

from ASCII import ASCII
from API import API
from Helpers import Helpers
from Configuration import Configuration

import lyricsgenius

log = logging.getLogger()
console = Console()

SPOTIFY_LIMIT = 50
QUSTIONARY_LIMIT = 36
API_BASE = "https://api.spotify.com"
API_VERSION = "v1"
API_PLAYER = urljoin(API_BASE, f"{API_VERSION}/me/player")
API_BASE_VERSION = urljoin(API_BASE, API_VERSION)


class Router(Configuration, API, Helpers, ASCII):
    """Available Spotr commands"""

    def refresh(self):
        """Refresh API key"""
        self.refresh_key()

    def next(self):
        """Play next track"""
        next_url = urljoin(API_PLAYER, "next")
        self.request("POST", next_url)
        self.current()

    def previous(self):
        """Play previous track"""
        previous_url = urljoin(API_PLAYER, "previous")
        self.request("POST", previous_url)
        self.current()

    def stop(self):
        """Stop/Pause playing"""
        stop_url = urljoin(API_PLAYER, "pause")
        self.request("PUT", stop_url)

    def start(self):
        """Start/Resume playing"""
        start_url = urljoin(API_PLAYER, "play")
        self.request("PUT", start_url)

    def play(self, json=None):
        """Play song or collection of songs"""
        play_url = urljoin(API_PLAYER, "play")
        self.request("PUT", play_url, json=json)

    def replay(self):
        """Replay/Restart currently playing song"""
        replay_url = urljoin(API_PLAYER, "seek").with_query(position_ms=0)
        self.request("PUT", replay_url)
        self.current()

    def seek(self, progress):
        """Seek posistion for track in seconds"""
        seek_url = urljoin(API_PLAYER, "seek").with_query(
            position_ms=int(progress) * 1000)
        self.request("PUT", seek_url)

    def web(self):
        """Open currently playing track in a broswer"""
        web_url = urljoin(API_PLAYER, "currently-playing")
        data = self.request("GET", web_url)
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
        shuffle_url = urljoin(API_PLAYER, "shuffle").with_query(state=state)
        self.request("PUT", shuffle_url)

    def volume(self, volume=None):
        """Ajust volume"""
        volume_url = urljoin(API_PLAYER, "volume").with_query(
            volume_percent=str(volume).replace("%", "")
        )
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
            "PUT", volume_url)
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
        playback_url = urljoin(API_PLAYER, "repeat").with_query(state=state)
        self.request("PUT", playback_url)

    def queue(self):
        """Get Queue"""
        queue_url = urljoin(API_PLAYER, "queue")
        data = self.request("GET", queue_url)
        for track in data["queue"]:
            console.print(f"[bold green]{track['name']}")

    def recent(self):
        """Get recently played tracks"""
        recent_url = urljoin(
            API_PLAYER, "recently-played").with_query(limit=QUSTIONARY_LIMIT)
        data = self.request(
            "GET", recent_url)

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
        playlist_url = urljoin(API_BASE_VERSION, "me", "playlists").with_query(
            limit=SPOTIFY_LIMIT
        )
        data = self.request(
            "GET", playlist_url)

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

        # Getting the list of playlists
        playlists_url = urljoin(API_BASE_VERSION, "me/playlists")
        data = self.request("GET", playlists_url, params={"limit": SPOTIFY_LIMIT})

        # Getting the currently playing song
        current_song_url = urljoin(API_PLAYER, "currently-playing")
        current_song = self.request("GET", current_song_url)

        # Check if there is a currently playing song
        if not current_song or 'item' not in current_song or not current_song['item']:
            console.print("[bold red]No song is currently playing.")
            return

        # Parsing the items to form choices for the user
        choices = self.parse_items(
            data,
            accessor=["items"],
            return_value=["id"],
            name_value=["name"],
            artists_value=False,
        )

        # User selects a playlist
        selected = questionary.select(
            "What playlist do you want to add the track to?",
            choices=choices,
            erase_when_done=True,
            use_arrow_keys=True,
            use_jk_keys=False,
        ).ask()

        if selected is None:
            return

        # Adding the current song to the selected playlist
        add_song_url = urljoin(API_BASE_VERSION, f"playlists/{selected}/tracks")
        self.request("POST", add_song_url, json={"uris": [current_song["item"]["uri"]]})

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

        search_url = urljoin(API_BASE_VERSION, "search").with_query(
            q=" ".join(query), type=search_type, limit=QUSTIONARY_LIMIT
        )

        data = self.request(
            "GET", search_url)

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

    def recommend(self):
        """Play random / recommended tracks based on recent tracks"""
        # Fetching recently played tracks
        recently_played_url = urljoin(API_PLAYER, "recently-played")
        recent = self.request("GET", recently_played_url, params={"limit": 5})

        seed_artists = []
        seed_genres = ["all"]  # Assuming 'all' is a valid genre for the Spotify API
        seed_tracks = []

        # Extracting seed values for recommendation
        for track in recent.get("items", []):
            seed_tracks.append(track["track"]["id"])
            seed_artists.append(track["track"]["artists"][0]["id"])

        # Fetching recommended tracks
        recommendations_url = urljoin(API_BASE_VERSION, "recommendations")
        recommended = self.request(
            "GET",
            recommendations_url,
            params={
                "seed_artists": ",".join(seed_artists),
                "seed_genres": ",".join(seed_genres),
                "seed_tracks": ",".join(seed_tracks),
                "limit": 5,
            }
        )

        results = []
        for track in recommended.get("tracks", []):
            results.append(track["uri"])

        if results:
            self.play(json={"uris": results})
            self.current()
        else:
            console.print("[bold red]No recommendations found based on recent tracks.")


    def ascii(self, width=100):
        """Ascii image for current track"""
        currently_playing_url = urljoin(API_PLAYER, "currently-playing")
        data = self.request("GET", currently_playing_url)

        # Check if there is data and a currently playing track
        if not data or 'item' not in data or not data['item']:
            print("No track is currently playing or track data is incomplete.")
            return

        track_image_url = data["item"]["album"]["images"][0]["url"]

        # Generate ASCII art based on the configuration
        ascii_str = (
            self.image_to_ascii_color(track_image_url, int(width))
            if eval(self.CONFIG["ASCII_IMAGE_COLOR"])
            else self.image_to_ascii(track_image_url, int(width))
        )

        # Print each line of the ASCII art
        print(ascii_str)


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

        currently_playing_url = urljoin(API_PLAYER, "currently-playing")
        data = self.request("GET", currently_playing_url)

        if not data or 'item' not in data or not data['item']:
            log.error("No track is currently playing or track data is incomplete.")
            return

        if data.get("currently_playing_type") != "track":
            log.error("Playing unsupported type - %s", data.get('currently_playing_type'))
            return

        current_track = data["item"]
        album_data = current_track["album"]
        artist_names = ", ".join([artist["name"]
                                 for artist in current_track["artists"]])
        track_duration_ms = current_track["duration_ms"]
        track_duration_m, track_duration_s = divmod(
            track_duration_ms // 1000, 60)
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
        {color_start('37')}Name{color_end}{color_start('32')} - {track_name}{color_end}
        {color_start('37')}Artits{color_end}{color_start('32')} - {artist_names}{color_end}
        {color_start('37')}Duration{color_end}{color_start('32')} - {track_duration_m} minutes {track_duration_s} seconds{color_end}
        {color_start('37')}Progress{color_end}{color_start('32')} - {progress_m} minutes {progress_s} seconds{color_end}
        {color_start('37')}Release date{color_end}{color_start('32')} - {track_release_date}{color_end}
        {color_start('37')}From{color_end}{color_start('32')} - {track_type} - {album_name}{color_end}
        {color_start('31')}Track details{color_end}
        {color_start('32')}------------------------------{color_end}
        {color_start('37')}Id{color_end}{color_start('32')} - {track_id}{color_end}
        {color_start('37')}URL{color_end}{color_start('32')} - {track_url}{color_end}
        {color_start('37')}Image{color_end}{color_start('32')} - {track_image}{color_end}
        """
        )

        if not eval(self.CONFIG["ANSI_COLORS"]):
            ansi_color_escape = re.compile(r"\x1b\[\d{1,2}m")
            strings = ansi_color_escape.sub("", strings)

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
                print(f"  {line.ljust(30)}  {
                      strings[i] if i < len(strings) else ''}")
            print()
        else:
            print()
            for line in strings:
                if eval(self.CONFIG["PRINT_DELAY_ACTIVE"]):
                    time.sleep(float(self.CONFIG["PRINT_DELAY"]))
                print(f"  {line}")
            print()

    def lyrics(self):
        """Show lyrics for the current track"""
        currently_playing_url = urljoin(API_PLAYER, "currently-playing")
        data = self.request("GET", currently_playing_url)

        if not data or 'item' not in data or not data['item']:
            log.error("No data available for the current track.")
            return

        current_track = data["item"]
        artist_names = ", ".join([artist["name"] for artist in current_track["artists"]])
        track_name = current_track["name"]

        genius = lyricsgenius.Genius("your_genius_api_token_here")
        song = genius.search_song(track_name, artist_names)

        if song:
            lyrics = song.lyrics
            # Remove annotations and other unwanted text
            clean_lyrics = re.sub(r'\[.*?\]', '', lyrics)  # Remove [...]
            # Optionally, remove 'Embed' and anything after it
            clean_lyrics = re.sub(r'Embed.*', '', clean_lyrics)
            print(clean_lyrics)
        else:
            print(f"No lyrics found for {track_name} by {artist_names}")

