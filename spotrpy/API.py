"""API class"""

import base64
import logging
import sys
import time
import webbrowser
import requests
from yarl import URL

log = logging.getLogger()
ACCOUNT_URL = URL.build(scheme="https", host="accounts.spotify.com")

class API:
    """API class for sending all requests"""

    def request(
        self, 
        method,
        url,
        headers=None,
        json=None
    ):
        """Spotr request, with deafult headers"""
        if headers is None:
            headers = {"Authorization": f"Bearer {self.CONFIG['key']}"}

        response = requests.request(method, url, headers=headers, json=json, timeout=10)

        if response.status_code in (401, 400):
            self.refresh_key()
            headers = {"Authorization": f"Bearer {self.CONFIG['key']}"}
            response = requests.request(method, url, headers=headers, json=json, timeout=10)

        if not response.ok:
            log.warning("[bold red]request error - status-code: %d", response.status_code)
            log.info(response.json())
            sys.exit()

        try:
            data = response.json()
        except ValueError:
            return None

        return data

    def refresh_key(self):
        """Refresh API key"""
        url = ACCOUNT_URL / "api" / "token"
        
        response = requests.post(
            url,
            data={
                "grant_type": "refresh_token",
                "refresh_token": self.CONFIG["refresh_token"],
            },
            headers={"Authorization": "Basic " + self.CONFIG["base_64"]},
            timeout=10,
        )
        if not response.ok:
            log.warning(
                "[bold red]request error - status-code: %d",
                response.status_code,
            )
            log.info(
                "[bold blue]Most likely something wrong with base_64 or refresh_token, try running 'spotr authorise'"
            )
            sys.exit()
        data = response.json()
        self.CONFIG["key"] = data["access_token"]
        self.write_config()

    def authorise(self):
        """Authenticate with Spotify API"""
        auth_url = ACCOUNT_URL / "authorize"
        token_url = ACCOUNT_URL / "api" / "token"

        client_id = str(input("Spotify-App Client id: "))
        client_secret = str(input("Spotify-App Client secret: "))

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

        print(
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

        self.CONFIG["refresh_token"] = access_token_response_data["refresh_token"]
        self.CONFIG["base_64"] = client_creds_b64.decode()
        self.write_config()
        print("All done!")
