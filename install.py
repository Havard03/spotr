""" Install script for spotr """

import os
import subprocess
import json
import sys

# Get current path
PATH = os.path.dirname(os.path.realpath(__file__))

CHECK_PATH = str(
    input(
        "Data will be written to the following PATH, is it correct? ("
        + PATH
        + ") y/n: "
    )
)
if CHECK_PATH.lower() != "y":
    sys.exit()

# check if .env and key.txt exists and creates them if not
print("Creating config.json")
if not os.path.exists(os.path.join(PATH + ".env")):
    open(os.path.join(PATH, "config.json"), "w", encoding="utf-8").close()

# make spot file executable
print("Making spot file executable...")
subprocess.run(["chmod", "u+x", os.path.join(PATH, "spotr")], check=True)

# install requirements
print("Installing spot requirements...")
subprocess.run(
    ["pip3", "install", "-r", os.path.join(PATH, "requirements.txt")], check=True
)

CONFIG = {
    "path": PATH,
    "refresh_token": "",
    "base_64": "",
    "key": "",
    "DEBUG": "False",
    "ASCII": "True",
}
with open(os.path.join(PATH, "config.json"), "w", encoding="utf-8") as file:
    json.dump(CONFIG, file, indent=4)

# start authetication process
print("Starting spotify authentication process...")
subprocess.run(["./spotr", "authorise"], check=True)

print("======================================")
print(
    "---  Add this folder to your PATH if you wish to execute spot commands anywhere---  "
)
print(
    f"---  This can be done by adding the following to your .rc file ([bold white]export PATH=$PATH:{PATH})---  "
)
print("======================================")
