import webbrowser
from urllib.parse import urljoin, urlencode

class Web():
    """ Web class """

    def __init__(self, spotr):
        # Command info
        self.info = {
            'name': 'Web',
            'description': 'Open currently playing track in a broswer',
            'arguments': [],
            'min_args': 0,
            'max_args': 0,
        }

        # Data URL
        self.URL = str(urljoin(spotr.API_PLAYER, "currently-playing"))

        # Arguments passed
        self.args = spotr.args

        # Unpack form spotr instance
        self.CONFIG = spotr.CONFIG
        self.request = spotr.request

    def execute(self):
        """Open currently playing track in a broswer"""
        data = self.request("GET", self.URL)

        if data is None:
            return
        
        webbrowser.open_new_tab(data["item"]["external_urls"]["spotify"])