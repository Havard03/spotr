import questionary
from urllib.parse import urljoin, urlencode

class Playback():
    """ Playback class """

    def __init__(self, spotr):
        # Command info
        self.info = {
            'name': 'Playback',
            'description': 'Set playback state',
            'arguments': [],
            'min_args': 0,
            'max_args': 0,
        }

        # Arguments passed
        self.args = spotr.args

        # Unpack form spotr instance
        self.CONFIG = spotr.CONFIG
        self.request = spotr.request
        self.API_PLAYER = spotr.API_PLAYER

    def execute(self):
        """Set playback state"""
        state = questionary.select(
            "Choose a play state",
            choices=["track", "context", "off"],
            erase_when_done=True,
            use_shortcuts=True,
        ).ask()

        if state is None:
            return
        
        self.request("PUT", str(f"{urljoin(self.API_PLAYER, 'repeat')}?{urlencode({'state': state})}"))


