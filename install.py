""" Install script for spotr """

import os
import sys
import subprocess

# Get current path
PATH = os.path.dirname(__file__)

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
print("Creating .env and key.txt files...")
if not os.path.exists(PATH + "/.env"):
    open(PATH + "/.env", "w", encoding='utf-8').close()
if not os.path.exists(PATH + "/key.txt"):
    open(PATH + "/key.txt", "w", encoding='utf-8').close()

# make spot file executable
print("Making spot file executable...")
subprocess.run(["chmod", "u+x", PATH + "/spotr"], check = True)

# install requirements
print("Installing spot requirements...")
subprocess.run(["pip3", "install", "-r", PATH + "/requirements.txt"], check = True)

# write template data to .env (Needed to run spot auth)
print("Writing template data to .env...")
env_data = f"""
#Environmental-variables
project_path="{PATH}/"
refresh_token=""
base_64=""
DEBUG="False"
""".replace(
    " ", ""
)
with open(PATH + "/.env", "w", encoding='utf-8') as f:
    f.write(env_data)

# start authetication process
print("Starting spotify authentication process...")
subprocess.run(["./spotr", "authorise"], check = True)

print(
    "---Add this folder to your PATH if you wish to execute spot commands anywhere---"
)
print(
    f"---This can be adding the following to your .rc file ([bold white]export PATH=$PATH:{PATH}---)"
)
