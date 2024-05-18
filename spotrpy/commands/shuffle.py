import questionary

from ..spotr import Spotr
from urllib.parse import urljoin, urlencode

class Shuffle(Spotr):
    """ Shuffle """

    description = "Toggle shuffle, on / off"

    def __init__(self, args):
        self.args = args
        Spotr.__init__(self)

    @staticmethod
    def add_arguments(parser):
        parser.add_argument(
            '-s', '--state', type=str, choices=["true", "false"], help="Toggle shuffle"
        )

    def execute(self):
        if not self.args.state:
            state = questionary.select(
                "Choose shuffle state",
                choices=["true", "false"],
                erase_when_done=True,
                use_shortcuts=True,
            ).ask()
        else:
            state = self.args.state

        if state is None:
            return
        
        self.request("PUT", str(f"{urljoin(self.API_PLAYER, 'shuffle')}?{urlencode({'state': state})}"))
