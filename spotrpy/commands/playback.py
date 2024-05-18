import questionary

from ..spotr import Spotr
from urllib.parse import urljoin, urlencode

class Playback(Spotr):
    """ Playback """

    description = "Set playback state"

    def __init__(self, args):
        self.args = args
        Spotr.__init__(self)

    @staticmethod
    def add_arguments(parser):
        parser.add_argument(
            '-s', '--state', type=str, choices=["track", "context", "off"], help="playback state"
        )

    def execute(self):
        if not self.args.state:
            state = questionary.select(
                "Choose a play state",
                choices=["track", "context", "off"],
                erase_when_done=True,
                use_shortcuts=True,
            ).ask()
        else:
            state = self.args.state

        if state is None:
            return
        
        self.request("PUT", str(f"{urljoin(self.API_PLAYER, 'repeat')}?{urlencode({'state': state})}"))
