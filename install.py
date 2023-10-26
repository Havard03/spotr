""" Install script for spotr """

import os
import subprocess
import json
import sys
import stat

# Get current path
PATH = os.path.dirname(os.path.realpath(__file__))

# check if .env and key.txt exists and creates them if not
print("Creating config.json")
if not os.path.exists(os.path.join(PATH + ".env")):
    open(os.path.join(PATH, "config.json"), "w", encoding="utf-8").close()


CONFIG = {
    "path": PATH,
    "refresh_token": "",
    "base_64": "",
    "key": "",
    "genius_access_token": "",
    "DEBUG": "False",
    "API_PROCESS_DELAY": "2",
    "ANSI_COLORS": "True",
    "USE_ASCII_LOGO": "True",
    "LOG_TRACK_URIS": "True",
    "ASCII_IMAGE": "True",
    "ASCII_IMAGE_SIZE_WIDTH": "50",
    "ASCII_IMAGE_COLOR": "True",
    "ASCII_IMAGE_UNICODE": "True",
    "ASCII_IMAGE_CHARS": '@%#*+=-:.`^",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$',
    "PRINT_DELAY_ACTIVE": "True",
    "PRINT_DELAY": "0.01",
    "IGNORED_FUNCTIONS": [
        "validate_config",
        "parse_functions",
        "rgb_to_ansi",
        "resize_image",
        "image_to_ascii",
        "image_to_ascii_color",
        "get_item",
        "parse_items",
        "refresh_key",
        "write_playlist",
        "write_config",
        "play",
        "path",
        "base_64",
        "request",
        "TOKEN",
        "CONFIG",
        "PLAYLIST",
        "__getstate__",
        "__class__",
        "__delattr__",
        "__dict__",
        "__dir__",
        "__doc__",
        "__eq__",
        "__format__",
        "__ge__",
        "__getattribute__",
        "__gt__",
        "__hash__",
        "__init__",
        "__init_subclass__",
        "__le__",
        "__lt__",
        "__module__",
        "__ne__",
        "__new__",
        "__reduce__",
        "__reduce_ex__",
        "__repr__",
        "__setattr__",
        "__sizeof__",
        "__str__",
        "__subclasshook__",
        "__weakref__",
        "authorise_spotify",
        "authorise_genius"
    ], }
with open(os.path.join(PATH, "config.json"), "w", encoding="utf-8") as file:
    json.dump(CONFIG, file, indent=4)

