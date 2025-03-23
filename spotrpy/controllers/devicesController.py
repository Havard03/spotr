import json
from urllib.parse import urljoin

from spotrpy.core.BaseController import BaseController


class DevicesController(BaseController):

    def run(self):
        data = self.request("GET", urljoin(self.API_PLAYER, "devices"))

        for device in data['devices']:
            print(device)
        
