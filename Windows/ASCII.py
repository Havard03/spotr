""" ASCII """

from io import BytesIO
import logging
from PIL import Image
import requests

# Logger for capturing and logging events
log = logging.getLogger()


class ASCII:
    """ASCII class for converting images to ASCII art."""

    def resize_image(self, image, new_width=100):
        """Resize image to a new width while maintaining aspect ratio."""
        # Calculate the new dimensions of the image, adjusting the height to maintain the aspect ratio.
        width, height = image.size
        ratio = height / width / 2.25  # The aspect ratio for ASCII art adjustment.
        new_height = int(new_width * ratio)
        resized_image = image.resize((new_width, new_height))
        return resized_image

    def image_to_ascii(self, image_url, desired_width=75):
        """Convert an image from a URL to ASCII art."""
        # Fetch the image from the URL and convert it to ASCII characters.
        response = requests.get(image_url, timeout=10)
        image_data = response.content

        image = Image.open(BytesIO(image_data))
        image = self.resize_image(image, desired_width)

        image = image.convert("L")  # Convert to grayscale.
        pixels = image.getdata()
        ascii_str = ""
        ascii_art = ""
        # Map each pixel value to an ASCII character from the configuration.
        for pixel_value in pixels:
            ascii_str += self.CONFIG["ASCII_IMAGE_CHARS"][
                max(
                    0, min(pixel_value // 16, len(self.CONFIG["ASCII_IMAGE_CHARS"]) - 1)
                )
            ]
        # Organize the ASCII string into lines to form the ASCII art.
        for i in range(0, len(ascii_str), int(desired_width)):
            row = ascii_str[i : i + int(desired_width)]
            ascii_art += row + "\n"
        return ascii_art

    def rgb_to_ansi(self, r, g, b):
        """Convert RGB color values to ANSI color codes for console output."""
        # This method is used to convert RGB values into ANSI codes for colored ASCII art.
        return f"\x1b[38;2;{r};{g};{b}m"

    def image_to_ascii_color(self, image_url, width=75):
        """Convert image to colored ASCII art."""
        # This method converts images to colored ASCII art by mapping each pixel's color to an ANSI code.

        response = requests.get(image_url, timeout=10)
        image = Image.open(BytesIO(response.content))

        # Resize the image while maintaining the aspect ratio.
        aspect_ratio = image.height / image.width
        new_height = int(width * aspect_ratio * 0.5)
        resized_image = image.resize((width, new_height))
        pixels = resized_image.convert("RGB").load()

        ascii_art = ""
        # Generate ASCII art line by line.
        for y in range(resized_image.height):
            for x in range(resized_image.width):
                try:
                    r, g, b, *_ = pixels[x, y]
                except TypeError:
                    # Handle exceptions during the conversion process.
                    LOG = (
                        log.exception("Something went wrong with image conversion")
                        if eval(self.CONFIG["DEBUG"])
                        else log.error("Something went wrong with image conversion")
                    )
                    exit()
                # Choose the ASCII character based on the configuration.
                char = "\u2588" if eval(self.CONFIG["ASCII_IMAGE_UNICODE"]) else "@"
                ascii_art += self.rgb_to_ansi(r, g, b) + char
            # Add a new line except for the last line.
            if y != resized_image.height - 1:
                ascii_art += "\n"

        # Reset the color at the end of the ASCII art.
        ascii_art += "\x1b[0m"

        return ascii_art
