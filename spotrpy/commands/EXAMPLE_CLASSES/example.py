from urllib.parse import urljoin, urlencode

class Example():
    """ Example class """

    def __init__(self, spotr):
        # Command info
        self.info = {
            'name': 'ascii',
            'description': 'Display ASCII art for the currently playing track.',
            'arguments': [],
            'min_args': 0,
            'max_args': 0,
        }

        # Data URL
        self.URL = str(urljoin(spotr.API_PLAYER, "some-url"))

        # Arguments passed
        self.args = spotr.args

        # Unpack form spotr instance
        self.CONFIG = spotr.CONFIG
        self.request = spotr.request

    def execute(self):
        """ Info """

        # Command call function

