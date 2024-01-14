from urllib.parse import urljoin, urlencode

class Stop():
    """ Stop class """

    def __init__(self, spotr):
        # Command info
        self.info = {
            'name': 'Stop',
            'description': 'Stop/Pause playing',
            'arguments': [],
            'min_args': 0,
            'max_args': 0,
        }

        # Data URL
        self.URL = str(urljoin(spotr.API_PLAYER, "pause"))

        # Arguments passed
        self.args = spotr.args

        # Unpack form spotr instance
        self.CONFIG = spotr.CONFIG
        self.request = spotr.request

    def execute(self):
        """Stop/Pause playing"""
        self.request("PUT", self.URL)

