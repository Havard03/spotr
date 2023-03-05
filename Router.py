from API import API
from Helpers import Helpers
from dotenv import load_dotenv, find_dotenv
from rich.console import Console
import questionary
import webbrowser, os, time

console = Console()
load_dotenv(find_dotenv())


class Router(API, Helpers):

    def refresh(self):
        self.refresh_key()
        return

    def next(self):
        self.request('POST', "https://api.spotify.com/v1/me/player/next")
        self.current()
        return

    def previous(self):
        self.request('POST', "https://api.spotify.com/v1/me/player/previous")
        return

    def stop(self):
        self.request('PUT', "https://api.spotify.com/v1/me/player/pause")
        return

    def start(self):
        self.request('PUT', "https://api.spotify.com/v1/me/player/play")
        return

    def replay(self):
        self.request('PUT', "https://api.spotify.com/v1/me/player/seek?position_ms=0")
        return
    
    def play(self, JSON=None):
        self.request('PUT', "https://api.spotify.com/v1/me/player/play", json=JSON)
        return

    def web(self):
        data = self.request('GET', "https://api.spotify.com/v1/me/player/currently-playing")
        if data == None: return
        webbrowser.open_new_tab(data['item']['external_urls']['spotify'])
        return

    def shuffle(self):
        state = questionary.select("Choose playback state", choices=['true', 'false'], erase_when_done=True, use_shortcuts=True).ask()
        self.request('PUT', f"https://api.spotify.com/v1/me/player/shuffle?state={state}")
        return

    def volume(self):
        volume = questionary.select("Choose volume precentage", choices=['25%', '50%', '75%', '100%'], erase_when_done=True, use_shortcuts=True).ask()
        self.request('PUT', f"https://api.spotify.com/v1/me/player/volume?volume_percent={volume.replace('%', '')}")
        return

    def playback(self):
        state = questionary.select("Choose a play state", choices=['track', 'context', 'off'], erase_when_done=True, use_shortcuts=True).ask()
        if answer is None: return
        self.request('PUT', f"https://api.spotify.com/v1/me/player/repeat?state={state}")
        return

    def queue(self):
        data = self.request('GET', "https://api.spotify.com/v1/me/player/queue")
        for track in data['queue']: console.print(f"[bold green]{track['name']}")
        return

    def recent(self):
        data = self.request('GET', "https://api.spotify.com/v1/me/player/recently-played?limit=36")
        choices = self.parseTracks(data['items'])
        
        answer = questionary.select(
            "What song do you want to play?",
            choices=choices,
            erase_when_done=True,
            use_shortcuts=True,
            use_arrow_keys=True,
            use_jk_keys=False
        ).ask()
        if answer is None: return
        
        answer = answer.split(' -- ')[0].strip()
        for track in data['items']:
            if track['track']['name'] == answer:
                JSON = {
                    "uris": [track['track']['uri']]
                }
                self.play(JSON=JSON)
                time.sleep(0.5)
                self.current()
                return

        return

    def playlist(self):
        data = self.request('GET', "https://api.spotify.com/v1/me/playlists?limit=50")
        choices= self.parseAlbums(data['items'])

        answer = questionary.select(
            "What playlist do you want to play?",
            choices=choices,
            erase_when_done=True,
            use_arrow_keys=True,
            use_jk_keys=False
        ).ask()
        if answer is None: return

        for playlist in data['items']:
            if playlist['name'] == answer:
                JSON = {
                    "context_uri": playlist['uri'], 
                    "offset": {
                        "position": "0"
                    }
                }
                self.play(JSON=JSON)
                time.sleep(0.5)
                self.current()
                return
        return
    
    def playlistadd(self):
        playlists = self.request('GET', "https://api.spotify.com/v1/me/playlists?limit=50")
        current_song = self.request('GET', "https://api.spotify.com/v1/me/player/currently-playing")
        choices= self.parseAlbums(playlist['items'])

        answer = questionary.select(
            "What playlist do you want to play?",
            choices=choices,
            erase_when_done=True,
            use_arrow_keys=True,
            use_jk_keys=False
        ).ask()
        if answer is None: return
        
        for playlist in playlists['items']:
            if playlist['name'] == answer:
                self.request("POST", f"https://api.spotify.com/v1/playlists/{playlist['id']}/tracks?uris={current_song['item']['uri']}")
                console.print(f"{current_song['item']['name']} was added to [bold green]{playlist['name']}")
                return
        return

    def search(self, *query):
        if query == (): raise TypeError
        data = self.request('GET', f"https://api.spotify.com/v1/search?q={' '.join(query)}&type=track&limit=36")
        choices = self.parseTracks(data['tracks']['items'], None)

        answer = questionary.select(
            "What song do you want to play?",
            choices=choices,
            erase_when_done=True,
            use_shortcuts=True,
            use_arrow_keys=True,
            use_jk_keys=False
        ).ask()
        if answer is None: return
        
        answer = answer.split(' -- ')[0].strip()
        for track in data['tracks']['items']:
            if track['name'] == answer:
                JSON = {
                    "uris": [track['uri']]
                }
                self.play(JSON=JSON)
                time.sleep(0.5)
                self.current()
                return        
        return
    
    def album(self, *query):
        if query == (): raise TypeError
        data = self.request('GET', f"https://api.spotify.com/v1/search?q={' '.join(query)}&type=album&limit=36")
        choices = self.parseTracks(data['albums']['items'], None)

        answer = questionary.select(
            "What album do you want to play?",
            choices=choices,
            erase_when_done=True,
            use_shortcuts=True,
            use_arrow_keys=True,
            use_jk_keys=False
        ).ask()
        if answer is None: return
        
        answer = answer.split(' -- ')[0].strip()
        for album in data['albums']['items']:
            if album['name'] == answer:
                JSON = {
                    "context_uri": album['uri'], 
                    "offset": {
                        "position": "0"
                    }
                }
                self.play(JSON=JSON)
                time.sleep(0.5)
                self.current()
                return        
        return

    def suprise(self):
        recent = self.request('GET', "https://api.spotify.com/v1/me/player/recently-played?limit=5")

        seed_arists = []
        seed_generes = ['all']
        seed_tracks = []

        for track in recent['items']:
            seed_tracks.append(track['track']['id'])
            seed_arists.append(track['track']['artists'][0]['id'])

        query = f"seed_arists={','.join(seed_arists)}"
        query += f"&seed_generes={','.join(seed_generes)}"
        query += f"&seed_tracks={','.join(seed_tracks)}"

        recommended = self.request('GET', f"https://api.spotify.com/v1/recommendations?{query}&limit=5")
        results=[]
        for track in recommended['tracks']:
            results.append(track['uri'])
        JSON = {
            "uris": results, 
            "offset": {
                "position": "0"
            }
        }

        self.play(JSON=JSON)
        time.sleep(0.5)
        self.current()
        return

    def current(self):
        data = self.request('GET', "https://api.spotify.com/v1/me/player/currently-playing")

        if data == None:
            console.log("[bold red]No data")
            return
        
        if data['item'] == None:
            self.current()
            return

        track_id = data['item']['id']
        track_name = data['item']['name']
        track_type = data['item']['album']['album_type']
        album_name = data['item']['album']['name']
        track_release_date = data['item']['album']['release_date']
        artist_names = ', '.join([artist['name'] for artist in data['item']['artists']])
        track_duration_m = int(data['item']['duration_ms'] / 1000 / 60)
        track_duration_s = int(data['item']['duration_ms'] / 1000 % 60)
        track_url = data['item']['external_urls']['spotify']
        progress_m = int(data['progress_ms'] / 1000 / 60)
        progress_s = int(data['progress_ms'] / 1000 % 60)

        console.print(f"""[green]

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
        
        """, justify="left")

        return