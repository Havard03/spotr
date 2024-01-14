from urllib.parse import urljoin, urlencode

class Start():
    """ Start class """

    def __init__(self, spotr):
        # Command info
        self.info = {
            'name': 'Start',
            'description': 'Start/Resume playing',
            'arguments': [],
            'min_args': 0,
            'max_args': 0,
        }

        # Data URL
        self.URL = str(urljoin(spotr.API_PLAYER, "play"))

        # Arguments passed
        self.args = spotr.args

        # Unpack form spotr instance
        self.CONFIG = spotr.CONFIG
        self.request = spotr.request

    def execute(self):
        """Start/Resume playing"""
        self.request("PUT", self.URL)


