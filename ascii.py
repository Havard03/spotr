""" ASCII """

from io import BytesIO
import requests
from PIL import Image

# Define the ASCII characters to use for the conversion
ASCII_CHARS = (
    '@%#*+=-:.`^",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'
)


def resize_image(image, new_width=100):
    """Rezise image"""
    width, height = image.size
    ratio = height / width / 2.25
    new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image


def image_to_ascii(image):
    """Convert image to ascii"""
    image = image.convert("L")  # Convert image to grayscale
    pixels = image.getdata()
    ascii_str = ""
    for pixel_value in pixels:
        ascii_str += ASCII_CHARS[pixel_value // 16]
    return ascii_str


def main(image_url, desired_width=100):
    """Do all convertions"""
    try:
        # Fetch the image data from the URL
        response = requests.get(image_url)
        image_data = response.content

        # Load the image from the fetched data
        image = Image.open(BytesIO(image_data))

        # Resize the image based on the desired width
        image = resize_image(image, desired_width)

        # Convert the resized image to ASCII
        ascii_str = image_to_ascii(image)

        # Print the ASCII art
        return ascii_str

    except Exception as error:
        print(f"Error: {error}")
