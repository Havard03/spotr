# Importing necessary libraries
import base64
import logging
import sys
import time
import webbrowser
import requests
from urllib.parse import urljoin

# Setting up a logger for the application
log = logging.getLogger()

# Constants for Spotify and Genius API URLs
ACCOUNT_BASE_URL_SPOTIFY = "https://accounts.spotify.com"
ACCOUNT_URL_GENIUS = "https://api.genius.com/oauth/authorize"


class API:
    """API class for sending all requests"""

    def request(self, method, url, headers=None, json=None):
        """Handles HTTP requests with default headers"""
        # Setting default authorization headers if not provided
        if headers is None:
            headers = {"Authorization": f"Bearer {self.CONFIG['key']}"}

        # Making the HTTP request
        response = requests.request(method, url, headers=headers, json=json, timeout=10)

        # Refresh the API key if unauthorized or bad request
        if response.status_code in (401, 400):
            self.refresh_key()
            headers = {"Authorization": f"Bearer {self.CONFIG['key']}"}
            response = requests.request(
                method, url, headers=headers, json=json, timeout=10
            )

        # Logging warning and exiting if the request is not successful
        if not response.ok:
            log.warning(
                "[bold red]request error - status-code: %d", response.status_code
            )
            log.info(response.json())
            sys.exit()

        try:
            # Attempt to parse and return the response data as JSON
            data = response.json()
        except ValueError:
            return None

        return data

    def refresh_key(self):
        """Refreshes the Spotify API key"""
        url = urljoin(ACCOUNT_BASE_URL_SPOTIFY, "api/token")

        # Making a request to refresh the API token
        response = requests.post(
            url,
            data={
                "grant_type": "refresh_token",
                "refresh_token": self.CONFIG["refresh_token"],
            },
            headers={"Authorization": "Basic " + self.CONFIG["base_64"]},
            timeout=10,
        )

        # Logging warning and exiting if request fails
        if not response.ok:
            log.warning(
                "[bold red]request error - status-code: %d",
                response.status_code,
            )
            log.info(
                "[bold blue]Most likely something wrong with base_64 or refresh_token, try running 'spotr authorise'"
            )
            sys.exit()

        # Updating the configuration with the new token
        data = response.json()
        self.CONFIG["key"] = data["access_token"]
        self.write_config()

    def authorise(self):
        """Authenticate with Spotify API and Genius API"""
        self.authorise_spotify()
        self.authorise_genius()

    def authorise_genius(self):
        """Collect Genius API client access token"""
        # Prompting user for Genius access token and storing it
        genius_access_token = str(input("Enter your Genius-App Client Access Token: "))
        self.CONFIG["genius_access_token"] = genius_access_token
        self.write_config()
        print("Genius Access Token stored successfully!")

    def authorise_spotify(self):
        """Authenticate with Spotify API"""
        # Prompting user for Spotify credentials and constructing authorization URL
        spotify_auth_url = urljoin(ACCOUNT_BASE_URL_SPOTIFY, "authorize")
        spotify_token_url = urljoin(ACCOUNT_BASE_URL_SPOTIFY, "api/token")

        spotify_client_id = str(input("Spotify-App Client id: "))
        spotify_client_secret = str(input("Spotify-App Client secret: "))

        auth_request = requests.get(
            spotify_auth_url,
            {
                "client_id": spotify_client_id,
                "response_type": "code",
                "redirect_uri": "https://www.google.com/",
                "scope": "playlist-read-collaborative playlist-read-private user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-recently-played playlist-modify-private playlist-modify-public",
            },
            timeout=10,
        )

        # Informing user about the authentication process and opening the URL
        print(
            "URL will open in 5 seconds, Accept the terms, Copy the code in the redirected URL, Then paste the code into the terminal"
        )
        time.sleep(5)
        webbrowser.open_new_tab(auth_request.url)

        # Prompting user for the authorization code and requesting access token
        auth_code = str(input("Enter code from the URL: "))

        client_creds = f"{spotify_client_id}:{spotify_client_secret}"
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
            url=spotify_token_url, data=payload, headers=headers, timeout=10
        )

        # Exiting if access token request fails
        if not access_token_request.ok:
            log.warning("Request error: %d", access_token_request.status_code)
            sys.exit()

        # Updating the configuration with the new token
        access_token_response_data = access_token_request.json()
        self.CONFIG["refresh_token"] = access_token_response_data["refresh_token"]
        self.CONFIG["base_64"] = client_creds_b64.decode()
        self.write_config()
        print("All done!")
