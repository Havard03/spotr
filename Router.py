""" Router Class """

import time
import webbrowser

import questionary
from dotenv import find_dotenv, load_dotenv
from rich.console import Console

from API import API
from Helpers import Helpers

console = Console()
load_dotenv(find_dotenv())


class Router(API, Helpers):
    """Available Spotr commands"""
    
    def refresh(self):
        """Refresh API key"""
        self.refresh_key()

    def next(self):
        """Play next track"""
        self.request("POST", "https://api.spotify.com/v1/me/player/next")
        self.current()

    def previous(self):
        """Play previous track"""
        self.request("POST", "https://api.spotify.com/v1/me/player/previous")

    def stop(self):
        """Stop/Pause playing"""
        self.request("PUT", "https://api.spotify.com/v1/me/player/pause")

    def start(self):
        """Start/Resume playing"""
        self.request("PUT", "https://api.spotify.com/v1/me/player/play")

    def replay(self):
        """Replay/Restart currently playing song"""
        self.request("PUT", "https://api.spotify.com/v1/me/player/seek?position_ms=0")

    def play(self, json=None):
        """Play song or collection of songs"""
        self.request("PUT", "https://api.spotify.com/v1/me/player/play", json=json)

    def web(self):
        """Open currently playing song in a broswer"""
        data = self.request(
            "GET", "https://api.spotify.com/v1/me/player/currently-playing"
        )
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
        self.request(
            "PUT", f"https://api.spotify.com/v1/me/player/shuffle?state={state}"
        )

    def volume(self):
        """Ajust volume"""
        volume = questionary.select(
            "Choose volume precentage",
            choices=["25%", "50%", "75%", "100%"],
            erase_when_done=True,
            use_shortcuts=True,
        ).ask()
        self.request(
            "PUT",
            f"https://api.spotify.com/v1/me/player/volume?volume_percent={volume.replace('%', '')}",
        )

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
        self.request(
            "PUT", f"https://api.spotify.com/v1/me/player/repeat?state={state}"
        )
        return

    def queue(self):
        """Get Queue"""
        data = self.request("GET", "https://api.spotify.com/v1/me/player/queue")
        for track in data["queue"]:
            console.print(f"[bold green]{track['name']}")

    def recent(self):
        """Get recently played tracks"""
        data = self.request(
            "GET", "https://api.spotify.com/v1/me/player/recently-played?limit=36"
        )
        choices = self.parse_tracks(data["items"])

        answer = questionary.select(
            "What song do you want to play?",
            choices=choices,
            erase_when_done=True,
            use_shortcuts=True,
            use_arrow_keys=True,
            use_jk_keys=False,
        ).ask()
        if answer is None:
            return

        answer = answer.split(" -- ")[0].strip()
        for track in data["items"]:
            if track["track"]["name"] == answer:
                json = {"uris": [track["track"]["uri"]]}
                self.play(json=json)
                time.sleep(0.5)
                self.current()
                return

    def playlist(self):
        """Choose a playlist"""
        data = self.request("GET", "https://api.spotify.com/v1/me/playlists?limit=50")
        choices = self.parse_albums(data["items"])

        answer = questionary.select(
            "What playlist do you want to play?",
            choices=choices,
            erase_when_done=True,
            use_arrow_keys=True,
            use_jk_keys=False,
        ).ask()
        if answer is None:
            return

        for playlist in data["items"]:
            if playlist["name"] == answer:
                json = {"context_uri": playlist["uri"], "offset": {"position": "0"}}
                self.play(json=json)
                time.sleep(0.5)
                self.current()
                return

    def playlistadd(self):
        """Add currently plating track to playlist"""

        playlists = self.request(
            "GET", "https://api.spotify.com/v1/me/playlists?limit=50"
        )
        current_song = self.request(
            "GET", "https://api.spotify.com/v1/me/player/currently-playing"
        )
        choices = self.parse_albums(playlists["items"])

        answer = questionary.select(
            "what playlist do you want to add track to?",
            choices=choices,
            erase_when_done=True,
            use_arrow_keys=True,
            use_jk_keys=False,
        ).ask()
        if answer is None:
            return

        for playlist in playlists["items"]:
            if playlist["name"] == answer:
                self.request(
                    "POST",
                    f"https://api.spotify.com/v1/playlists/{playlist['id']}/tracks?uris={current_song['item']['uri']}",
                )
                console.print(
                    f"{current_song['item']['name']} was added to [bold green]{playlist['name']}"
                )
                return

    def search(self, *query):
        """Search for tracks on spotify"""
        if not query:
            raise TypeError
        data = self.request(
            "GET",
            f"https://api.spotify.com/v1/search?q={' '.join(query)}&type=track&limit=36",
        )
        choices = self.parse_tracks(data["tracks"]["items"])

        answer = questionary.select(
            "What song do you want to play?",
            choices=choices,
            erase_when_done=True,
            use_shortcuts=True,
            use_arrow_keys=True,
            use_jk_keys=False,
        ).ask()
        if answer is None:
            return

        answer = answer.split(" -- ")[0].strip()
        for track in data["tracks"]["items"]:
            if track["name"] == answer:
                json = {"uris": [track["uri"]]}
                self.play(json=json)
                time.sleep(0.5)
                self.current()
                return

    def album(self, *query):
        """Search for albums on spotify"""
        if not query:
            raise TypeError
        data = self.request(
            "GET",
            f"https://api.spotify.com/v1/search?q={' '.join(query)}&type=album&limit=36",
        )
        choices = self.parse_tracks(data["albums"]["items"])

        answer = questionary.select(
            "What album do you want to play?",
            choices=choices,
            erase_when_done=True,
            use_shortcuts=True,
            use_arrow_keys=True,
            use_jk_keys=False,
        ).ask()
        if answer is None:
            return

        answer = answer.split(" -- ")[0].strip()
        for album in data["albums"]["items"]:
            if album["name"] == answer:
                json = {"context_uri": album["uri"], "offset": {"position": "0"}}
                self.play(json=json)
                time.sleep(0.5)
                self.current()
                return

    def suprise(self):
        """Play random / recommended track based on recent tracks"""
        recent = self.request(
            "GET", "https://api.spotify.com/v1/me/player/recently-played?limit=5"
        )

        seed_arists = []
        seed_generes = ["all"]
        seed_tracks = []

        for track in recent["items"]:
            seed_tracks.append(track["track"]["id"])
            seed_arists.append(track["track"]["artists"][0]["id"])

        query = f"seed_arists={','.join(seed_arists)}"
        query += f"&seed_generes={','.join(seed_generes)}"
        query += f"&seed_tracks={','.join(seed_tracks)}"

        recommended = self.request(
            "GET", f"https://api.spotify.com/v1/recommendations?{query}&limit=5"
        )
        results = []
        for track in recommended["tracks"]:
            results.append(track["uri"])
        json = {"uris": results, "offset": {"position": "0"}}

        self.play(json=json)
        time.sleep(0.5)
        self.current()

    def current(self):
        """Display information about current track"""
        data = self.request(
            "GET", "https://api.spotify.com/v1/me/player/currently-playing"
        )

        if data is None:
            console.log("[bold red]No data")
            return
        if data["item"] is None:
            self.current()
            return

        track_id = data["item"]["id"]
        track_name = data["item"]["name"]
        track_type = data["item"]["album"]["album_type"]
        album_name = data["item"]["album"]["name"]
        track_release_date = data["item"]["album"]["release_date"]
        artist_names = ", ".join([artist["name"] for artist in data["item"]["artists"]])
        track_duration_m = int(data["item"]["duration_ms"] / 1000 / 60)
        track_duration_s = int(data["item"]["duration_ms"] / 1000 % 60)
        track_url = data["item"]["external_urls"]["spotify"]
        progress_m = int(data["progress_ms"] / 1000 / 60)
        progress_s = int(data["progress_ms"] / 1000 % 60)

        console.print(
            f"""[green]

        ⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣤⣶⣶⣶⣶⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀  [bold red]Current track[/bold red]
        ⠀⠀⠀⠀⢀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡀⠀⠀⠀⠀  ------------------------------
        ⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀  [bold white]Name[/bold white]          -  {track_name}
        ⠀⢀⣾⣿⡿⠿⠛⠛⠛⠉⠉⠉⠉⠛⠛⠛⠿⠿⣿⣿⣿⣿⣿⣷⡀⠀  [bold white]Artits[/bold white]        -  {artist_names}
        ⠀⣾⣿⣿⣇⠀⣀⣀⣠⣤⣤⣤⣤⣤⣀⣀⠀⠀⠀⠈⠙⠻⣿⣿⣷⠀  [bold white]Duration[/bold white]      -  {track_duration_m} minutes {track_duration_s} seconds
        ⢠⣿⣿⣿⣿⡿⠿⠟⠛⠛⠛⠛⠛⠛⠻⠿⢿⣿⣶⣤⣀⣠⣿⣿⣿⡄  [bold white]Progress[/bold white]      -  {progress_m} minutes {progress_s} seconds
        ⢸⣿⣿⣿⣿⣇⣀⣀⣤⣤⣤⣤⣤⣄⣀⣀⠀⠀⠉⠛⢿⣿⣿⣿⣿⡇  [bold white]Release date[/bold white]  -  {track_release_date} 
        ⠘⣿⣿⣿⣿⣿⠿⠿⠛⠛⠛⠛⠛⠛⠿⠿⣿⣶⣦⣤⣾⣿⣿⣿⣿⠃  [bold white]From[/bold white]          -  {track_type} - {album_name}
        ⠀⢿⣿⣿⣿⣿⣤⣤⣤⣤⣶⣶⣦⣤⣤⣄⡀⠈⠙⣿⣿⣿⣿⣿⡿⠀  
        ⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⣿⣿⡿⠁⠀  [bold red]Track details[/bold red]
        ⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀⠀  ------------------------------
        ⠀⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠁⠀⠀⠀⠀  [bold white]Id[/bold white]  - {track_id}
        ⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⠛⠿⠿⠿⠿⠛⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀  [bold white]URL[/bold white] - {track_url}
        
        """,
            justify="left",
        )
