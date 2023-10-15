""" ASCII """

from io import BytesIO
import logging
from PIL import Image
import requests

log = logging.getLogger()

class ASCII:
    """ASCII class"""

    def resize_image(self, image, new_width=100):
        """Rezise image"""
        width, height = image.size
        ratio = height / width / 2.25
        new_height = int(new_width * ratio)
        resized_image = image.resize((new_width, new_height))
        return resized_image

    def image_to_ascii(self, image_url, desired_width=75):
        """Convert image to ascii"""

        response = requests.get(image_url, timeout=10)
        image_data = response.content

        image = Image.open(BytesIO(image_data))
        image = self.resize_image(image, desired_width)

        image = image.convert("L")
        pixels = image.getdata()
        ascii_str = ""
        ascii_art = ""
        for pixel_value in pixels:
            ascii_str += self.CONFIG["ASCII_IMAGE_CHARS"][
                max(
                    0, min(pixel_value // 16, len(self.CONFIG["ASCII_IMAGE_CHARS"]) - 1)
                )
            ]
        for i in range(0, len(ascii_str), int(desired_width)):
            row = ascii_str[i : i + int(desired_width)]
            ascii_art += row + "\n"
        return ascii_art

    def rgb_to_ansi(self, r, g, b):
        """Convert RGB color values to ANSI color codes for console."""
        return f"\x1b[38;2;{r};{g};{b}m"

    def image_to_ascii_color(self, image_url, width=75):
        """Convert image to ASCII art with color."""
        
        response = requests.get(image_url, timeout=10)
        image = Image.open(BytesIO(response.content))

        aspect_ratio = image.height / image.width
        new_height = int(width * aspect_ratio * 0.5)
        resized_image = image.resize((width, new_height))
        pixels = resized_image.convert("RGB").load()

        ascii_art = ""
        for y in range(resized_image.height):
            for x in range(resized_image.width):
                try:
                    r, g, b, *_ = pixels[x, y]
                except TypeError:
                    LOG = (
                        log.exception("Something went wrong with image convertion")
                        if eval(self.CONFIG["DEBUG"])
                        else log.error("Something went wrong with image convertion")
                    )
                    exit()
                char = "\u2588" if eval(self.CONFIG["ASCII_IMAGE_UNICODE"]) else "@"
                ascii_art += self.rgb_to_ansi(r, g, b) + char
            if y != resized_image.height - 1:
                ascii_art += "\n"

        ascii_art += "\x1b[0m"

        return ascii_art
