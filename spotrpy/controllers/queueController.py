from urllib.parse import urljoin

from spotrpy.core.BaseController import BaseController 


class queueController(BaseController):

    def run(self):
        self.fetch()
        for track in self.response["queue"]:
            self.console.print(f"{track['name']}")

    def fetch(self):
        self.response = self.request("GET", urljoin(self.API_PLAYER, "queue"))
