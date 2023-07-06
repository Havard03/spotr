""" Router Class """

import time
import webbrowser

import questionary
import yarl
from rich.console import Console
from yarl import URL

from ascii import *
from API import API
from Helpers import Helpers

console = Console()

SPOTIFY_LIMIT = 50
QUSTIONARY_LIMIT = 36
API_BASE = yarl.URL("api.spotify.com")
API_VERSION = yarl.URL("v1")
API_PLAYER = yarl.URL("https://api.spotify.com") / str(API_VERSION) / "me" / "player"
API_BASE_VERSION = yarl.URL("https://api.spotify.com") / str(API_VERSION)


class Router(API, Helpers):
    """Available Spotr commands"""

    def refresh(self):
        """Refresh API key"""
        self.refresh_key()

    def next(self):
        """Play next track"""
        self.request("POST", str(URL(API_PLAYER / "next")))
        self.current()

    def previous(self):
        """Play previous track"""
        self.request("POST", str(URL(API_PLAYER / "previous")))
        self.current()

    def stop(self):
        """Stop/Pause playing"""
        self.request("PUT", str(URL(API_PLAYER / "pause")))

    def start(self):
        """Start/Resume playing"""
        self.request("PUT", str(URL(API_PLAYER / "play")))

    def replay(self):
        """Replay/Restart currently playing song"""
        self.request("PUT", str(URL(API_PLAYER / "seek").with_query(position_ms=0)))

    def seek(self, progress):
        """Seek posistion for track in seconds"""
        self.request(
            "PUT",
            str(URL(API_PLAYER / "seek").with_query(position_ms=int(progress) * 1000)),
        )

    def play(self, json=None):
        """Play song or collection of songs"""
        self.request("PUT", str(URL(API_PLAYER / "play")), json=json)

    def web(self):
        """Open currently playing song in a broswer"""
        data = self.request("GET", str(URL(API_PLAYER / "currently-playing")))
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
        self.request("PUT", str(URL(API_PLAYER / "shuffle").with_query(state=state)))

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
                URL(API_PLAYER / "volume").with_query(
                    volume_percent=str(volume).replace("%", "")
                )
            ),
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
        self.request("PUT", str(URL(API_PLAYER / "repeat").with_query(state=state)))
        return

    def queue(self):
        """Get Queue"""
        data = self.request("GET", str(URL(API_PLAYER / "queue")))
        for track in data["queue"]:
            console.print(f"[bold green]{track['name']}")

    def recent(self):
        """Get recently played tracks"""
        data = self.request(
            "GET",
            str(URL(API_PLAYER / "recently-played").with_query(limit=QUSTIONARY_LIMIT)),
        )
        choices = self.parse_tracks(data["items"], key="track")

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

        answer = answer.replace(" ", "")
        for track in data["items"]:
            track_name = f"{track['track']['name']}--{','.join(artist['name'] for artist in track['track']['artists'])}".replace(
                " ", ""
            )
            if track_name == answer:
                json = {"uris": [track["track"]["uri"]]}
                self.play(json=json)
                time.sleep(0.5)
                self.current()
                return

    def playlist(self):
        """Choose a playlist"""
        data = self.request(
            "GET",
            str(
                URL(API_BASE_VERSION / "me" / "playlists").with_query(
                    limit=SPOTIFY_LIMIT
                )
            ),
        )
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
            "GET",
            str(URL(API_BASE_VERSION / "me/playlists").with_query(limit=SPOTIFY_LIMIT)),
        )
        current_song = self.request("GET", str(URL(API_PLAYER / "currently-playing")))
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
                    str(
                        URL(
                            API_BASE_VERSION / "playlists" / playlist["id"] / "tracks"
                        ).with_query(uris=current_song["item"]["uri"])
                    ),
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
            str(
                URL(API_BASE_VERSION / "search").with_query(
                    q=" ".join(query), type="track", limit=QUSTIONARY_LIMIT
                )
            ),
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

        answer = answer.replace(" ", "")
        for track in data["tracks"]["items"]:
            track_name = f"{track['name']}--{','.join(artist['name'] for artist in track['artists'])}".replace(
                " ", ""
            )
            if track_name == answer:
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
            str(
                URL(API_BASE_VERSION / "search").with_query(
                    q=" ".join(query), type="album", limit=QUSTIONARY_LIMIT
                )
            ),
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

        answer = answer.replace(" ", "")
        for album in data["albums"]["items"]:
            album_name = f"{album['name']}--{','.join(artist['name'] for artist in album['artists'])}".replace(
                " ", ""
            )
            if album_name == answer:
                json = {"context_uri": album["uri"], "offset": {"position": "0"}}
                self.play(json=json)
                time.sleep(0.5)
                self.current()
                return

    def suprise(self):
        """Play random / recommended track based on recent tracks"""
        recent = self.request(
            "GET", str(URL(API_PLAYER / "recently-played").with_query(limit=5))
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
                URL(API_BASE_VERSION / "recommendations").with_query(
                    {
                        "seed_arists": ",".join(seed_arists),
                        "seed_generes": ",".join(seed_generes),
                        "seed_tracks": ",".join(seed_tracks),
                        "limit": 5,
                    }
                )
            ),
        )
        results = []
        for track in recommended["tracks"]:
            results.append(track["uri"])
        json = {"uris": results, "offset": {"position": "0"}}

        self.play(json=json)
        time.sleep(0.5)
        self.current()

    def ascii(self, width=100):
        """Ascii image for current track"""
        data = self.request("GET", str(URL(API_PLAYER / "currently-playing")))
        ascii_str = main(data["item"]["album"]["images"][0]["url"], int(width))

        for i in range(0, len(ascii_str), int(width)):
            row = ascii_str[i : i + int(width)]
            print(row)

    def current(self):
        """Display information about current track"""
        data = self.request("GET", str(URL(API_PLAYER / "currently-playing")))

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
        track_image = data["item"]["album"]["images"][0]["url"]
        progress_m = int(data["progress_ms"] / 1000 / 60)
        progress_s = int(data["progress_ms"] / 1000 % 60)

        if eval(self.CONFIG["ASCII"]):
            width = 75
            ascii_str = main(data["item"]["album"]["images"][0]["url"], width)
            strings = [
                "[bold red]Current track[/bold red]",
                "[green]------------------------------[/green]",
                f" [bold white]Name[/bold white][green]          -  {track_name}[/green]",
                f" [bold white]Artits[/bold white][green]        -  {artist_names}[/green]",
                f" [bold white]Duration[/bold white][green]      -  {track_duration_m} minutes {track_duration_s} seconds[/green]",
                f" [bold white]Progress[/bold white][green]      -  {progress_m} minutes {progress_s} seconds[/green]",
                f" [bold white]Release date[/bold white][green]  -  {track_release_date}[/green]",
                f" [bold white]From[/bold white][green]          -  {track_type} - {album_name}[/green]",
                "[bold red]Track details[/bold red]",
                "[green]------------------------------[/green]",
                f" [bold white]Id[/bold white][green]  - {track_id}[/green]",
                f" [bold white]URL[/bold white][green] - {track_url}[/green]",
                f" [bold white]Image[/bold white][green] - {track_image}[/green]",
            ]

            y = 0
            for i in range(0, len(ascii_str), int(width)):
                row = ascii_str[i : i + int(width)]
                if i >= 675 and y < len(strings):
                    console.print(f"     [white]{row}[/white]    {strings[y]}")
                    y = y + 1
                elif i == 0:
                    print("")
                    print(f"     {row}")
                elif i == 2400:
                    print(f"     {row}")
                    print("")
                else:
                    print(f"     {row}")
        else:
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

    """Shorthands"""
    prev = previous
    vol = volume
