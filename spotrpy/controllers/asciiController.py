import os,sys,time
from urllib.parse import urljoin

from spotrpy.core.BaseController import BaseController
from spotrpy.util.ASCII import ASCII


class asciiController(BaseController, ASCII):

    def run(self):
        self.fetch()
        if self.args.width is None:
            width, height = os.get_terminal_size()
        else:
            width = self.args.width

        ascii_str = (
            self.image_to_ascii_color(
                self.response["item"]["album"]["images"][0]["url"], int(width)
            )
            if eval(self.CONFIG["ASCII_IMAGE_COLOR"])
            else self.image_to_ascii(
                self.response["item"]["album"]["images"][0]["url"], int(width)
            )
        )
        lines = ascii_str.splitlines()
        for line in lines:
            print(line)

    def fetch(self):
        self.response = self.request("GET", urljoin(self.API_PLAYER, "currently-playing"))
        if self.response is None or self.response["item"] is None:
            self.log.error("No data")
            sys.exit()
            
    def idle(self):
        self.run()
        id = self.response['item']['id']
        try:
            while True:
                self.fetch()
                
                if not id == self.response['item']['id']:
                    print("\033c")
                    self.run()
                    id = self.response['item']['id']
            
                time.sleep(5)
        except KeyboardInterrupt:
            sys.exit()

