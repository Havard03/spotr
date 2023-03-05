from dotenv import load_dotenv, find_dotenv
from rich.console import Console
import subprocess, webbrowser, base64, os, requests, time

load_dotenv(find_dotenv())
console = Console()

class API():

    def __init__(self):
        try:
            self.path = os.environ["project_path"]
            self.refresh_token = os.environ["refresh_token"]
            self.base_64 = os.environ["base_64"]
            with open(os.environ["project_path"]+"key.txt") as file: self.TOKEN = file.read()
        except KeyError:
            console.log("[bold red]Enviorment-Variables are not set!")
            pass

    def request(self, TYPE, URL, HEADERS=None, json=None):
        if HEADERS is None: HEADERS = {"Authorization": f"Bearer {self.TOKEN}"}

        response = requests.request(TYPE, URL, headers=HEADERS, json=json)
        
        if (response.status_code == 401 or response.status_code == 400):
            self.refresh_key()
            with open(os.environ["project_path"]+"key.txt") as file: self.TOKEN = file.read()
            HEADERS = {"Authorization": f"Bearer {self.TOKEN}"}
            response = requests.request(TYPE, URL, headers=HEADERS, json=json)

        if (not response.ok):
            console.log(response.json())
            console.log(f"# [bold red]request error | status-code: {response.status_code}")
            exit()

        try:
            response.json()
        except ValueError:
            return
        else:
            return response.json()

    def refresh_key(self):
        URL = "https://accounts.spotify.com/api/token"

        response = requests.post(URL,
            data={"grant_type": "refresh_token", "refresh_token": self.refresh_token},
            headers={"Authorization": "Basic " + self.base_64}
        )

        if (not response.ok): 
            console.log(f"# [bold red]request error | status-code: {response.status_code}")
            console.log("# [bold green]Most likely something wrong with base_64 or refresh_token, try running '[bold red]spot auth[/bold red]'")
            exit()

        data = response.json()

        with open(self.path + "key.txt", "w") as f:
            f.write(data["access_token"])
            f.close()
            
        return

    def authorise(self):
        AUTH_URL = 'https://accounts.spotify.com/authorize'
        TOKEN_URL = 'https://accounts.spotify.com/api/token'
        
        CLIENT_ID = str(input("Client id: "))
        CLIENT_SECRET = str(input("Client secret: "))
                            
        auth_request = requests.get(AUTH_URL, {
            'client_id': CLIENT_ID,
            'response_type': 'code',
            'redirect_uri': 'https://www.google.com/',
            'scope': 'playlist-read-collaborative playlist-read-private user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-recently-played playlist-modify-private playlist-modify-public',
        })

        console.print(f'URL will open in 5 seconds, Accept the terms, Copy the code in the redirected URL, Then paste the code into the terminal')
        time.sleep(5)
        webbrowser.open_new_tab(auth_request.url)
        
        auth_code = str(input("Enter code from the URL: "))
        
        client_creds = f"{CLIENT_ID}:{CLIENT_SECRET}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic %s" % client_creds_b64.decode()
        }
        payload = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": "https://www.google.com/",
        }
        
        access_token_request = requests.post(url=TOKEN_URL, data=payload, headers=headers)

        if (not access_token_request.ok):
            console.log(f"Request error: {access_token_request.status_code}")
            exit()

        access_token_response_data = access_token_request.json()

        try:
            self.path

            env_data = f"""
            #Enviorment-variables
            project_path="{self.path}"
            refresh_token="{access_token_response_data['refresh_token']}"
            base_64="{client_creds_b64.decode()}"
            """.replace(" ",  "")

            with open(self.path + ".env", "w") as f:
                f.write(env_data)

        except:
            PATH = os.path.dirname(__file__)

            check_path = str(input("Data will be written to the following PATH, is it correct? (" + PATH + ") y/n: "))
            if check_path.lower() != "y":
                exit()

            if not os.path.exists(PATH + "/.env") or os.path.exists(PATH + "/key.txt"):
                os.system("touch " + PATH + "/.env")
                os.system("touch " + PATH + "/key.txt")

            env_data = f"""
            #Enviorment-variables
            project_path="{PATH}/"
            refresh_token="{access_token_response_data["refresh_token"]}"
            base_64="{client_creds_b64.decode()}"
            """.replace(" ",  "")

            with open(PATH + "/.env", "w") as f:
                f.write(env_data)
