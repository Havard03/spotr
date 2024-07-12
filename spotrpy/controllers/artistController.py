import re
import sys
import time
import textwrap
import questionary
from urllib.parse import urljoin, urlencode

from spotrpy.core.BaseController import BaseController
from spotrpy.util.ASCII import ASCII
from spotrpy.util.Helpers import Helpers


class artistController (BaseController, Helpers, ASCII):

    def run(self):
        if self.args.artist:
            self.response = self.request(
                "GET",
                str(
                    f"{urljoin(self.API_BASE_VERSION, 'search')}?{urlencode({'q': ' '.join(self.args.artist), 'type': 'artist', 'limit': self.QUSTIONARY_LIMIT})}"
                )
            )
        else:
            current = self.request("GET", urljoin(self.API_PLAYER, "currently-playing"))
            if current is None:
                self.log.error("No track currently playing")
                sys.exit()
            self.response = self.request("GET", urljoin(self.API_BASE_VERSION, f"artists/{current['item']['artists'][0]['id']}"))

        if self.args.artist:
            choices = self.parse_items(
                self.response,
                accessor=(["artists", "items"] if self.args.artist else None),
                name_value=["name"],
                artists_value=False,
            )

            selected = questionary.select(
                "Select artist",
                choices=choices,
                erase_when_done=True,
                use_shortcuts=True,
                use_arrow_keys=True,
                use_jk_keys=False,
            ).ask()
            if selected is None:
                return       
        else:
            selected = self.response

        color_start = "\x1b[{}m".format
        color_end = "\x1b[0m"

        strings = textwrap.dedent(
                f"""
            {color_start('31')}Artist{color_end}
            {color_start('32')}------------------------------{color_end}
            {color_start('37')}Name{color_end}{color_start('32')}           -  {selected['name']}{color_end}
            {color_start('37')}Popularity{color_end}{color_start('32')}     -  {selected['popularity']}{color_end}
            {color_start('37')}Genres{color_end}{color_start('32')}         -  {", ".join(selected['genres'])}{color_end}
            {color_start('37')}Followers{color_end}{color_start('32')}      -  {selected['followers']['total']}{color_end}

            {color_start('31')}Details{color_end}
            {color_start('32')}------------------------------{color_end}
            {color_start('37')}URL{color_end}{color_start('32')}            - {selected['href']}{color_end}
            {color_start('37')}URI{color_end}{color_start('32')}            - {selected['uri']}{color_end}
            {color_start('37')}Image{color_end}{color_start('32')}          - {selected['images'][0]['url']}{color_end}
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
                        selected["images"][0]["url"], int(width)
                    )
                    if eval(self.CONFIG["ASCII_IMAGE_COLOR"])
                    else self.image_to_ascii(
                        selected["images"][0]["url"], int(width)
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

