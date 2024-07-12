import base64
import sys
import requests

from urllib.parse import urljoin

class API():
    """ API """

    def __initAPI__(self):
        self.SPOTIFY_LIMIT      = 50
        self.QUSTIONARY_LIMIT   = 36
        self.API_VERSION        = "v1"
        self.API_BASE           = "api.spotify.com"
        self.ACCOUNT_URL        = "https://accounts.spotify.com" 
        self.API_PLAYER         = urljoin("https://api.spotify.com", f"{self.API_VERSION}/me/player/")
        self.API_BASE_VERSION   = urljoin("https://api.spotify.com", f"{self.API_VERSION}/")

    def request(
        self, 
        method,
        url,
        headers=None,
        json=None
    ):
        """ Spotify API request """

        if headers is None: headers = {"Authorization": f"Bearer {self.CONFIG['key']}"}
        
        response = requests.request(method, url, headers=headers, json=json, timeout=10)

        if not response.ok:
            status_code = response.status_code

            self.log.error(f"Requst error - {status_code}")

            if status_code in (401, 400):                
                self.__refresh_token()
                
                headers     = {"Authorization": f"Bearer {self.CONFIG['key']}"}
                response    = requests.request(method, url, headers=headers, json=json, timeout=10)

        try:
            data = response.json()
        except ValueError:
            data = None

        return data

    def __refresh_token(self):
        """ Refresh Spotify API token """

        self.log.debug(f"Refreshing API-Token")
        url = urljoin(self.ACCOUNT_URL, "api/token")
        
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
            self.log.critical(f"Request error - status-code: {response.status_code}")
            self.log.critical("Indication of invalid refresh_token, or base_64")

            sys.exit()

        data = response.json()
        self.CONFIG["key"] = data["access_token"]
        self.write_config()

    def authorise(self, client_id=None, client_secret=None):
        """ Authorise CLI with Spotify API """

        auth_url  = urljoin(self.ACCOUNT_URL, "authorize")
        token_url = urljoin(self.ACCOUNT_URL, "api/token")

        if not client_id: client_id         = str(input("Spotify-App Client id: "))
        if not client_secret: client_secret = str(input("Spotify-App Client secret: "))

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

        print("\nGo to the Following URL, Accept the terms, Copy the code in the redirected URL, Then paste the code into the terminal\n")
        print(f"\n{auth_request.url}\n")

        auth_code           = str(input("Enter code from the URL: "))
        client_creds        = f"{client_id}:{client_secret}"
        client_creds_b64    = base64.b64encode(client_creds.encode())

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
            self.log.warning("Request error: %d", access_token_request.status_code)
            sys.exit()

        access_token_response_data      = access_token_request.json()
        self.CONFIG["refresh_token"]    = access_token_response_data["refresh_token"]
        self.CONFIG["base_64"]          = client_creds_b64.decode()

        self.write_config()
        print("All done!")
