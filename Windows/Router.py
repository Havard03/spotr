# Importing necessary modules
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

# Importing custom modules for ASCII art, API handling, Helpers, and Configuration
from ASCII import ASCII
from API import API
from Helpers import Helpers
from Configuration import Configuration

import lyricsgenius  # Importing lyricsgenius for fetching song lyrics

# Setting up logging and console for rich text formatting
log = logging.getLogger()
console = Console()

# Constants for Spotify API limits
SPOTIFY_LIMIT = 50
QUSTIONARY_LIMIT = 36
API_BASE = "https://api.spotify.com"
API_VERSION = "v1"
API_PLAYER = urljoin(API_BASE, f"{API_VERSION}/me/player")
API_BASE_VERSION = urljoin(API_BASE, API_VERSION)

class Router(Configuration, API, Helpers, ASCII):
    """Class containing available Spotr commands, inheriting from Configuration, API, Helpers, and ASCII."""

    # Refresh the API key
    def refresh(self):
        self.refresh_key()

    # Play the next track
    def next(self):
        next_url = urljoin(API_PLAYER, "next")
        self.request("POST", next_url)
        self.current()

    # Play the previous track
    def previous(self):
        previous_url = urljoin(API_PLAYER, "previous")
        self.request("POST", previous_url)
        self.current()

    # Stop or pause the current playback
    def stop(self):
        stop_url = urljoin(API_PLAYER, "pause")
        self.request("PUT", stop_url)

    # Start or resume the current playback
    def start(self):
        start_url = urljoin(API_PLAYER, "play")
        self.request("PUT", start_url)

    # Play a song or a collection of songs
    def play(self, json=None):
        play_url = urljoin(API_PLAYER, "play")
        self.request("PUT", play_url, json=json)

    # Replay or restart the currently playing song
    def replay(self):
        replay_url = urljoin(API_PLAYER, "seek").with_query(position_ms=0)
        self.request("PUT", replay_url)
        self.current()

    # Seek a specific position in the current track
    def seek(self, progress):
        seek_url = urljoin(API_PLAYER, "seek").with_query(
            position_ms=int(progress) * 1000)
        self.request("PUT", seek_url)

    # Open the current track in a web browser
    def web(self):
        web_url = urljoin(API_PLAYER, "currently-playing")
        data = self.request("GET", web_url)
        if data is None:
            return
        webbrowser.open_new_tab(data["item"]["external_urls"]["spotify"])

    # Toggle shuffle mode on or off
    def shuffle(self):
        state = questionary.select(
            "Choose playback state",
            choices=["true", "false"],
            erase_when_done=True,
            use_shortcuts=True,
        ).ask()
        shuffle_url = urljoin(API_PLAYER, "shuffle").with_query(state=state)
        self.request("PUT", shuffle_url)

    # Adjust the volume
    def volume(self, volume=None):
        volume_url = urljoin(API_PLAYER, "volume").with_query(
            volume_percent=str(volume).replace("%", "")
        )
        if volume is None:
            volume = questionary.select(
                "Choose volume percentage",
                choices=["25%", "50%", "75%", "100%"],
                erase_when_done=True,
                use_shortcuts=True,
            ).ask()
        else:
            if int(volume) < 0:
                volume = 0
            elif int(volume) > 100:
                volume = 100
        self.request("PUT", volume_url)
    vol = volume  # Alias for the volume function

    # Set the playback state
    def playback(self):
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

    # Get the current queue
    def queue(self):
        queue_url = urljoin(API_PLAYER, "queue")
        data = self.request("GET", queue_url)
        for track in data["queue"]:
            console.print(f"[bold green]{track['name']}")

    # Retrieve and play recently played tracks
    def recent(self):
        recent_url = urljoin(
            API_PLAYER, "recently-played").with_query(limit=QUSTIONARY_LIMIT)
        data = self.request("GET", recent_url)
        choices = self.parse_items(
            data, accessor=["items"], return_value=["track", "uri"],
            name_value=["track", "name"], artists_value=["track", "artists"]
        )
        selected = questionary.select(
            "What song do you want to play?",
            choices=choices, erase_when_done=True, use_shortcuts=True,
            use_arrow_keys=True, use_jk_keys=False).ask()
        if selected is None:
            return
        json_data = {"uris": [selected]}
        self.play(json=json_data)
        self.current()

    # Playlist method to choose and play a playlist
    def playlist(self):
        """Choose a playlist and play it."""
        # Construct URL to fetch the user's playlists
        playlist_url = urljoin(API_BASE_VERSION, "me", "playlists").with_query(limit=SPOTIFY_LIMIT)
        data = self.request("GET", playlist_url)

        # Parse the playlist data into a format suitable for display in a selection prompt
        choices = self.parse_items(
            data,
            accessor=["items"],
            return_value=["uri"],
            name_value=["name"],
            artists_value=False,
        )

        # Prompt the user to select a playlist
        selected = questionary.select(
            "What playlist do you want to play?",
            choices=choices,
            erase_when_done=True,
            use_arrow_keys=True,
            use_jk_keys=False,
        ).ask()

        # Exit if no playlist is selected
        if selected is None:
            return

        # Create JSON payload to play the selected playlist and execute play command
        json = {"context_uri": selected, "offset": {"position": "0"}}
        self.play(json=json)
        self.current()

    # Playlistadd method to add currently playing track to a selected playlist
    def playlistadd(self):
        """Add the currently playing track to a selected playlist."""
        # Fetch user's playlists
        playlists_url = urljoin(API_BASE_VERSION, "me/playlists")
        data = self.request("GET", playlists_url, params={"limit": SPOTIFY_LIMIT})

        # Fetch currently playing song
        current_song_url = urljoin(API_PLAYER, "currently-playing")
        current_song = self.request("GET", current_song_url)

        # Check if a song is currently playing
        if not current_song or 'item' not in current_song or not current_song['item']:
            console.print("[bold red]No song is currently playing.")
            return

        # Parse playlist data for selection prompt
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

        # Exit if no playlist is selected
        if selected is None:
            return

        # Add the current song to the selected playlist
        add_song_url = urljoin(API_BASE_VERSION, f"playlists/{selected}/tracks")
        self.request("POST", add_song_url, json={"uris": [current_song["item"]["uri"]]})

    # Search method to search for items on Spotify
    def search(self, *query):
        """Search for tracks, playlists, or albums on Spotify."""
        # Check if a query is provided
        if not query:
            raise TypeError

        # Define search types and their corresponding parameters
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

        # Create a search URL and fetch results
        search_url = urljoin(API_BASE_VERSION, "search").with_query(
            q=" ".join(query), type=search_type, limit=QUSTIONARY_LIMIT
        )
        data = self.request("GET", search_url)


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
        """Play random or recommended tracks based on the user's recent listening history."""
        # Fetching the user's recently played tracks from Spotify
        recently_played_url = urljoin(API_PLAYER, "recently-played")
        recent = self.request("GET", recently_played_url, params={"limit": 5})

        # Initializing lists to hold seed values for artist and track IDs
        seed_artists = []
        seed_genres = ["all"]  # Using a generic genre seed; 'all' is assumed to be a valid genre
        seed_tracks = []

        # Extracting artist and track IDs from recently played tracks to use as seeds
        for track in recent.get("items", []):
            seed_tracks.append(track["track"]["id"])
            seed_artists.append(track["track"]["artists"][0]["id"])

        # Constructing the URL for fetching recommendations based on seeds
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

        # Extracting the URIs of recommended tracks
        results = []
        for track in recommended.get("tracks", []):
            results.append(track["uri"])

        # Checking if there are recommended tracks, then play them, otherwise print a message
        if results:
            self.play(json={"uris": results})  # Play the recommended tracks
            self.current()  # Update the current track display
        else:
            console.print("[bold red]No recommendations found based on recent tracks.")  # No recommendations found


    def ascii(self, width=100):
        """Generate and display an ASCII art representation of the currently playing track's album cover."""
        # Fetch data about the currently playing track from Spotify
        currently_playing_url = urljoin(API_PLAYER, "currently-playing")
        data = self.request("GET", currently_playing_url)

        # Check if there is currently a track playing and if the data is complete
        if not data or 'item' not in data or not data['item']:
            print("No track is currently playing or track data is incomplete.")
            return  # Exit the function if no track data is available

        # Extract the URL of the album cover image from the track data
        track_image_url = data["item"]["album"]["images"][0]["url"]

        # Generate ASCII art from the album cover image
        # The method used depends on the ASCII_IMAGE_COLOR configuration setting
        ascii_str = (
            self.image_to_ascii_color(track_image_url, int(width))
            if eval(self.CONFIG["ASCII_IMAGE_COLOR"])
            else self.image_to_ascii(track_image_url, int(width))
        )

        # Print the generated ASCII art to the console
        print(ascii_str)


    def current(self):
        """Display information about the current track."""
        # Checking if this method is called directly and applying an API process delay
        if inspect.stack()[1].filename == inspect.getfile(inspect.currentframe()):
            timeout = float(self.CONFIG["API_PROCESS_DELAY"])
            num_updates = int(timeout * 10)
            update_increment = 1 / 10
            # Progress bar for the API process delay
            with tqdm(total=num_updates, desc="API Process Delay", unit="update", leave=True) as pbar:
                for i in range(num_updates):
                    time.sleep(update_increment)
                    pbar.update(1)
            print("\033[F\033[K", end="")  # Clearing the progress bar line

        # Fetching data about the currently playing track
        currently_playing_url = urljoin(API_PLAYER, "currently-playing")
        data = self.request("GET", currently_playing_url)

        # Error handling if no track is currently playing or if the data is incomplete
        if not data or 'item' not in data or not data['item']:
            log.error("No track is currently playing or track data is incomplete.")
            return

        # Handling unsupported types of currently playing items
        if data.get("currently_playing_type") != "track":
            log.error("Playing unsupported type - %s", data.get('currently_playing_type'))
            return

        # Extracting relevant information about the current track
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

        # Formatting strings for console output with color codes
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

        # Removing ANSI color codes if ANSI colors are disabled in the configuration
        if not eval(self.CONFIG["ANSI_COLORS"]):
            ansi_color_escape = re.compile(r"\x1b\[\d{1,2}m")
            strings = ansi_color_escape.sub("", strings)

        strings = strings.strip().splitlines()

        # Displaying ASCII art or logo alongside the track details
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
            # Displaying the track details without ASCII art
            print()
            for line in strings:
                if eval(self.CONFIG["PRINT_DELAY_ACTIVE"]):
                    time.sleep(float(self.CONFIG["PRINT_DELAY"]))
                print(f"  {line}")
            print()

    def lyrics(self):
        """Show lyrics for the current track using the Genius API."""
        # Fetching data about the currently playing track from Spotify
        currently_playing_url = urljoin(API_PLAYER, "currently-playing")
        data = self.request("GET", currently_playing_url)

        # Error handling if no data is available for the current track
        if not data or 'item' not in data or not data['item']:
            log.error("No data available for the current track.")
            return

        # Extracting the artist names and track name from the current track data
        current_track = data["item"]
        artist_names = ", ".join([artist["name"] for artist in current_track["artists"]])
        track_name = current_track["name"]

        # Initializing the Genius API client with the API token
        genius = lyricsgenius.Genius("your_genius_api_token_here")
        # Searching for the song on Genius using the track and artist names
        song = genius.search_song(track_name, artist_names)

        # Checking if the song's lyrics are found and then displaying them
        if song:
            lyrics = song.lyrics
            # Removing annotations and other unwanted text from the lyrics
            clean_lyrics = re.sub(r'\[.*?\]', '', lyrics)  # Removing bracketed text like [Chorus]
            clean_lyrics = re.sub(r'Embed.*', '', clean_lyrics)  # Optionally removing 'Embed' and subsequent text
            print(clean_lyrics)
        else:
            # Message displayed if lyrics are not found
            print(f"No lyrics found for {track_name} by {artist_names}")
