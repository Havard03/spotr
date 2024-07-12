import questionary
from urllib.parse import urljoin, urlencode

from spotrpy.core.BaseController import BaseController


class shuffleController(BaseController):

    def run(self):
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
