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
    os.system("touch " + PATH + "/.env")
if not os.path.exists(PATH + '/key.txt'):
    os.system("touch " + PATH + "/key.txt")
    
#make spot file executable
print("Making spot file executable...")
os.system("chmod u+x " + PATH + '/spotr')

#install requirements
print("Installing spot requirements...")
os.system("pip3 install -r " + PATH + "/requirements.txt")

#write template data to .env (Needed to run spot auth)
print("Writing template data to .env...")
env_data = f"""
#Enviorment-variables
project_path="{PATH}/"
refresh_token=""
base_64=""
""".replace(" ", "")
with open(PATH + '/.env', 'w') as f:
    f.write(env_data)

#start authetication process
print("Starting spotify authentication process...")
os.system("./spotr authorise")

from rich.console import Console
console = Console()

console.print("[bold red]Add this folder to your PATH if you wish to execute spot commands anywhere")
console.print(f"[bold red]This can be adding the following to your .rc file ([bold white]export PATH=$PATH:{PATH}[/bold white])")




    
