import questionary
from urllib.parse import urljoin, urlencode

class Volume():
    """ Volume class """

    def __init__(self, spotr):
        # Command info
        self.info = {
            'name': 'Volume',
            'description': 'Display ASCII art for the currently playing track.',
            'arguments': ['Volume (in percentage)'],
            'min_args': 0,
            'max_args': 1,
        }

        # Arguments passed
        self.args = spotr.args

        # Unpack form spotr instance
        self.CONFIG = spotr.CONFIG
        self.request = spotr.request
        self.API_PLAYER = spotr.API_PLAYER

    def execute(self, volume=None):
        """Ajust volume"""
        if volume is None:
            volume = questionary.select(
                "Choose volume precentage",
                choices=["25%", "50%", "75%", "100%"],
                erase_when_done=True,
                use_shortcuts=True,
            ).ask()
        else:
            if int(volume) < 0:
                volume = 0
            elif int(volume) > 100:
                volume = 100
        self.request(
            "PUT",
            str(
                f"{urljoin(self.API_PLAYER, 'volume')}?{urlencode({'volume_percent': str(volume).replace('%', '')})}"
            ),
        )

