""" API class """

import base64
import logging
import os
import sys
import time
import webbrowser

import requests
import yarl
from dotenv import find_dotenv, load_dotenv
from rich.logging import RichHandler
from yarl import URL

load_dotenv(find_dotenv())
log = logging.getLogger()


ACCOUNT_URL = URL.build(scheme="https", host="accounts.spotify.com")

if eval(os.environ["DEBUG"]):
    logging.basicConfig(
        level="NOTSET",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(markup=True, rich_tracebacks=True)],
    )
else:
    logging.basicConfig(
        level="INFO",
        datefmt="[%X]",
        format="%(message)s",
        handlers=[RichHandler(markup=True)],
    )


class API:
    """API class for sending all requests"""

    def __init__(self):
        try:
            self.path = os.environ["project_path"]
            self.refresh_token = os.environ["refresh_token"]
            self.base_64 = os.environ["base_64"]
            with open(os.path.join(self.path, "key.txt"), encoding="utf-8") as file:
                self.TOKEN = file.read()
        except KeyError:
            log.critical("[bold red]Enviorment-Variables are not set!")
            ERROR: eval = (
                log.exception("[bold blue]Try running the authorise command")
                if eval(os.environ["DEBUG"])
                else log.info("[bold blue]Try running the authorise command")
            )

    def request(self, method, url, headers=None, json=None):
        """Spotr request, with deafult headers"""
        if headers is None:
            headers = {"Authorization": f"Bearer {self.TOKEN}"}

        response = requests.request(method, url, headers=headers, json=json, timeout=10)

        if response.status_code in (401, 400):
            self.refresh_key()
            with open(
                os.path.join(os.environ["project_path"], "key.txt"), encoding="utf-8"
            ) as file:
                self.TOKEN = file.read()
            headers = {"Authorization": f"Bearer {self.TOKEN}"}
            response = requests.request(
                method, url, headers=headers, json=json, timeout=10
            )

        if not response.ok:
            log.warning(
                "[bold red]request error - status-code: %d", response.status_code
            )
            log.info(response.json())
            sys.exit()

        try:
            response.json()
        except ValueError:
            return None

        return response.json()

    def refresh_key(self):
        """Refresh API key"""
        url = ACCOUNT_URL / "api" / "token"
        response = requests.post(
            url,
            data={"grant_type": "refresh_token", "refresh_token": self.refresh_token},
            headers={"Authorization": "Basic " + self.base_64},
            timeout=10,
        )
        if not response.ok:
            log.warning(
                "[bold red]request error - status-code: %d",
                response.status_code,
            )
            log.info(
                "[bold blue]Most likely something wrong with base_64 or refresh_token, try running [bold green]spotr authorise[/bold green]"
            )
            sys.exit()
        data = response.json()
        with open(os.path.join(self.path, "key.txt"), "w", encoding="utf-8") as f:
            f.write(data["access_token"])
            f.close()

    def authorise(self):
        """Authenticate with Spotify API"""
        auth_url = ACCOUNT_URL / "authorize"
        token_url = ACCOUNT_URL / "api" / "token"

        client_id = str(input("Client id: "))
        client_secret = str(input("Client secret: "))

        auth_request = requests.get(
            auth_url,
            {
                "client_id": client_id,
                "response_type": "code",
                "redirect_uri": "https://www.google.com/",
                "scope": "playlist-read-collaborative playlist-read-private user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-recently-played playlist-modify-private playlist-modify-public",
            },
            timeout=10,
        )

        log.info(
            "URL will open in 5 seconds, Accept the terms, Copy the code in the redirected URL, Then paste the code into the terminal"
        )
        time.sleep(5)
        webbrowser.open_new_tab(auth_request.url)

        auth_code = str(input("Enter code from the URL: "))

        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic %s" % client_creds_b64.decode(),
        }
        payload = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": "https://www.google.com/",
        }

        access_token_request = requests.post(
            url=token_url, data=payload, headers=headers, timeout=10
        )

        if not access_token_request.ok:
            log.warning("Request error: %d", access_token_request.status_code)
            sys.exit()

        access_token_response_data = access_token_request.json()

        try:
            env_data = f"""
            #Environmental-variables
            project_path="{self.path}"
            refresh_token="{access_token_response_data['refresh_token']}"
            base_64="{client_creds_b64.decode()}"
            DEBUG="False"
            """.replace(
                " ", ""
            )

            with open(os.path.join(self.path, ".env"), "w", encoding="utf-8") as f:
                f.write(env_data)

        except AttributeError:
            path = os.path.dirname(__file__)

            check_path = str(
                input(
                    f"Data will be written to the following PATH, is it correct? ({path}) y/n: "
                )
            )
            if check_path.lower() != "y":
                sys.exit()

            if not os.path.exists(os.path.join(path, ".env")) or os.path.exists(
                os.path.join(path, "key.txt")
            ):
                open(os.path.join(path, "key.txt"), "w", encoding="utf-8").close()
                open(os.path.join(path, ".env"), "w", encoding="utf-8").close()

            env_data = f"""
            #Environmental-variables
            project_path="{path}/"
            refresh_token="{access_token_response_data["refresh_token"]}"
            base_64="{client_creds_b64.decode()}"
            DEBUG="False"
            """.replace(
                " ", ""
            )

            with open(os.path.join(path, ".env"), "w", encoding="utf-8") as f:
                f.write(env_data)
