from urllib.parse import urljoin, urlencode

class Replay():
    """ Replay class """

    def __init__(self, spotr):
        # Command info
        self.info = {
            'name': 'Replay',
            'description': 'Replay/Restart currently playing track',
            'arguments': [],
            'min_args': 0,
            'max_args': 0,
        }

        # Data URL
        self.URL = str(f"{urljoin(spotr.API_PLAYER, 'seek')}?{urlencode({'position_ms': 0})}")

        # Arguments passed
        self.args = spotr.args

        # Unpack form spotr instance
        self.CONFIG = spotr.CONFIG
        self.request = spotr.request

    def execute(self):
        """Replay/Restart currently playing track"""
        self.request("PUT", self.URL)

