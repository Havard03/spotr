import re
import time
import sys
import textwrap
from urllib.parse import urljoin

from spotrpy.core.BaseController import BaseController
from spotrpy.util.ASCII import ASCII

class currentController(BaseController, ASCII):

    def run(self):
        self.fetch()

        current_track                       = self.response["item"]
        album_data                          = current_track["album"]
        artist_names                        = ", ".join([artist["name"] for artist in current_track["artists"]])
        track_duration_ms                   = current_track["duration_ms"]
        track_duration_m, track_duration_s  = divmod(track_duration_ms // 1000, 60)
        progress_ms                         = self.response["progress_ms"]
        progress_m, progress_s              = divmod(progress_ms // 1000, 60)
        track_id                            = current_track["id"]
        track_name                          = current_track["name"]
        track_type                          = album_data["album_type"]
        album_name                          = album_data["name"]
        track_release_date                  = album_data["release_date"]
        track_url                           = current_track["external_urls"]["spotify"]
        track_image                         = album_data["images"][0]["url"]

        color_start = "\x1b[{}m".format
        color_end = "\x1b[0m"

        strings = textwrap.dedent(
            f"""
        {color_start('31')}Current track{color_end}
        {color_start('32')}------------------------------{color_end}
        {color_start('37')}Name{color_end}{color_start('32')}          -  {track_name}{color_end}
        {color_start('37')}Artits{color_end}{color_start('32')}        -  {artist_names}{color_end}
        {color_start('37')}Duration{color_end}{color_start('32')}      -  {track_duration_m} minutes {track_duration_s} seconds{color_end}
        {color_start('37')}Progress{color_end}{color_start('32')}      -  {progress_m} minutes {progress_s} seconds{color_end}
        {color_start('37')}Release date{color_end}{color_start('32')}  -  {track_release_date}{color_end}
        {color_start('37')}From{color_end}{color_start('32')}          -  {track_type} - {album_name}{color_end}
        
        {color_start('31')}Track details{color_end}
        {color_start('32')}------------------------------{color_end}
        {color_start('37')}Id{color_end}{color_start('32')}     - {track_id}{color_end}
        {color_start('37')}URL{color_end}{color_start('32')}    - {track_url}{color_end}
        {color_start('37')}Image{color_end}{color_start('32')}  - {track_image}{color_end}
        """
        )

        ansi_color_escape = re.compile(r"\x1b\[\d{1,2}m")
        strings_no_color = ansi_color_escape.sub("", strings)
        if not eval(self.CONFIG["ANSI_COLORS"]):
            strings = strings_no_color

        strings = strings.strip().splitlines()

        if eval(self.CONFIG["ASCII_IMAGE"]) or eval(self.CONFIG["USE_ASCII_LOGO"]):
            if eval(self.CONFIG["ASCII_IMAGE"]):
                width = self.CONFIG["ASCII_IMAGE_SIZE_WIDTH"]
                ascii_str = (
                    self.image_to_ascii_color(
                        self.response["item"]["album"]["images"][0]["url"], int(width)
                    )
                    if eval(self.CONFIG["ASCII_IMAGE_COLOR"])
                    else self.image_to_ascii(
                        self.response["item"]["album"]["images"][0]["url"], int(width)
                    )
                ).splitlines()
            elif eval(self.CONFIG["USE_ASCII_LOGO"]):
                ascii_str = self.CONFIG["ASCII_LOGO"]
            print()
            for i, line in enumerate(ascii_str):
                if eval(self.CONFIG["PRINT_DELAY_ACTIVE"]):
                    time.sleep(float(self.CONFIG["PRINT_DELAY"]))
                print(f"  {line}  {strings[i] if i < len(strings) else ''}")
            print()
        else:
            print()
            for line in strings:
                if eval(self.CONFIG["PRINT_DELAY_ACTIVE"]):
                    time.sleep(float(self.CONFIG["PRINT_DELAY"]))
                print(f"  {line}")
            print()

    def fetch(self):
        response = self.request("GET", urljoin(self.API_PLAYER, "currently-playing"))

        if response is None or response["item"] is None:
            self.log.error(f'No data - {response}')
            sys.exit() 
        elif response["currently_playing_type"] not in ("track"):
            self.log.error("Playing unsupported type - %s", response['currently_playing_type'])
            sys.exit()
        else:
            self.response = response


