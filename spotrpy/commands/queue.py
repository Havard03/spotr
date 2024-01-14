from urllib.parse import urljoin, urlencode

class Queue():
    """ Queue class """

    def __init__(self, spotr):
        # Command info
        self.info = {
            'name': 'Queue',
            'description': 'Get songs in Queue',
            'arguments': [],
            'min_args': 0,
            'max_args': 0,
        }

        # Data URL
        self.URL = str(urljoin(spotr.API_PLAYER, "queue"))

        # Arguments passed
        self.args = spotr.args

        # Unpack form spotr instance
        self.CONFIG = spotr.CONFIG
        self.request = spotr.request
        self.console = spotr.console

    def execute(self):
        """Get songs in Queue"""
        data = self.request("GET", self.URL)

        for track in data["queue"]:
            self.console.print(f"[bold green]{track['name']}")


