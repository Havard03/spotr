import os
import subprocess

#Get current path
PATH = os.path.dirname(__file__)

check_path = str(input("Data will be written to the following PATH, is it correct? (" + PATH + ") y/n: "))
if check_path.lower() != "y":
    exit()

#check if .env and key.txt exists and creates them if not
print("Creating .env and key.txt files...")
if not os.path.exists(PATH + '/.env'):
    open(PATH + '/.env', "w").close()
if not os.path.exists(PATH + '/key.txt'):
    open(PATH + '/key.txt', "w").close()
    
#make spot file executable
print("Making spot file executable...")
subprocess.run(['chmod','u+x', PATH+"/spotr"])

#install requirements
print("Installing spot requirements...")
subprocess.run(['pip3', 'install',  '-r', PATH + "/requirements.txt"])

#write template data to .env (Needed to run spot auth)
print("Writing template data to .env...")
env_data = f"""
#Enviorment-variables
project_path="{PATH}/"
refresh_token=""
base_64=""
debug="False"
""".replace(" ", "")
with open(PATH + '/.env', 'w') as f:
    f.write(env_data)

#start authetication process
print("Starting spotify authentication process...")
subprocess.run(['./spotr', 'authorise'])

from rich.console import Console
console = Console()

console.log("[bold blue]Add this folder to your PATH if you wish to execute spot commands anywhere")
console.log(f"[bold blue]This can be adding the following to your .rc file ([bold white]export PATH=$PATH:{PATH}[/bold white])")




    
