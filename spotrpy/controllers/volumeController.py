import questionary
from urllib.parse import urljoin, urlencode

from spotrpy.core.BaseController import BaseController

class volumeController(BaseController):

    def run(self):
        if self.args.percentage is None:
            volume = questionary.select(
                "Choose volume precentage",
                choices=["25%", "50%", "75%", "100%"],
                erase_when_done=True,
                use_shortcuts=True,
            ).ask()
        else:
            volume = self.args.percentage

        self.request(
            "PUT",
            str(
                f"{urljoin(self.API_PLAYER, 'volume')}?{urlencode({'volume_percent': str(volume).replace('%', '')})}"
            ),
        )
