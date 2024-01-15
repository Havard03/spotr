import questionary
from urllib.parse import urljoin, urlencode

class Shuffle():
    """ Shuffle class """

    def __init__(self, spotr):
        # Command info
        self.info = {
            'name': 'Shuffle',
            'description': 'Display ASCII art for the currently playing track.',
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
        """Toggle shuffle, on / off"""
        state = questionary.select(
            "Choose playback state",
            choices=["true", "false"],
            erase_when_done=True,
            use_shortcuts=True,
        ).ask()
        
        self.request("PUT", str(f"{urljoin(self.API_PLAYER, 'shuffle')}?{urlencode({'state': state})}"))
