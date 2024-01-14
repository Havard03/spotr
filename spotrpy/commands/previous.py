from urllib.parse import urljoin, urlencode

class Previous():
    """ Previous class """

    def __init__(self, spotr):
        # Command info
        self.info = {
            'name': 'Previous',
            'description': 'Play previous track',
            'arguments': [],
            'min_args': 0,
            'max_args': 0,
        }

        # Data URL
        self.URL = str(urljoin(spotr.API_PLAYER, "previous"))

        # Arguments passed
        self.args = spotr.args

        # Unpack form spotr instance
        self.CONFIG = spotr.CONFIG
        self.request = spotr.request

    def execute(self):
        """Play previous track"""
        self.request("POST", self.URL)
