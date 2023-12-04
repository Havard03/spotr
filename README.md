
<h1 align="center">Spotr - A spotify tool for the terminal</h1>

<p align="center">
 <a href="https://github.com/Havard03/spotr/graphs/contributors">
  <img src="https://img.shields.io/github/contributors/Havard03/spotr.svg?style=for-the-badge"></a>
 <a href="https://github.com/Havard03/spotr/network/members">
  <img src="https://img.shields.io/github/forks/Havard03/spotr.svg?style=for-the-badge"></a>
 <a href="https://github.com/Havard03/spotr/stargazers">
  <img src="https://img.shields.io/github/stars/Havard03/spotr.svg?style=for-the-badge"></a>
 <a href="https://github.com/Havard03/spotr/issues">
  <img src="https://img.shields.io/github/issues/Havard03/spotr.svg?style=for-the-badge"></a>
 <a href="https://github.com/Havard03/spotr/blob/master/LICENSE.txt">
  <img src="https://img.shields.io/github/license/Havard03/spotr.svg?style=for-the-badge"></a>
</p>

<p align="center">
A very simple CLI for controlling your spotify on the fly in the terminal. 
<br>
Made in python for simplicity
</p>

<img align="center" width="100%" src="https://user-images.githubusercontent.com/58250866/228016062-60718528-212a-49c9-ac3d-c81bb43d3278.gif">

<h1 align="center" style="border-bottom: none">NEWS</h1>
<p align="center">
It is now possible to bring the pictures into the terminal with image to ascii convertion!
<br>
Use "ascii" command to show image
<br>
Or set ASCII variable to True in config.json to replace spotify logo with ascii image for "current" command
</p>

<img align="center" width="100%" src="https://github.com/Havard03/spotr/assets/58250866/7c36407d-e335-468b-ad44-59cc89f30b2e">


<h1 align="center" style="border-bottom: none">Installation</h1>

<h3>Windows<h3>
<p>

1. Go to Releases and download the newest version of the installer.

2. Follow the instructions to install.

3. Go to <a href="https://developer.spotify.com/dashboard/">Spotify dashboard</a> and register an app.

4. In options, set Redirect URIs to "https://www.google.com/".

5. Past in client-id and client-secret in the designated fields. Continue the installation.

6. Go to <a href="https://genius.com/api-clients/new">Genius dashboard</a> and register an app, set Redirect URIs to "https://www.google.com/".

7. Add the path to system environment variables and run spotr in the terminal and enjoy.


</p>
<h3>Manual</h3>
</p>

Due to registration on pyPI being temporarily disabled, you currently have to do a bit more manual work until it opens again

1. Clone repo to your computer and cd into folder

2. Build files "python3 setup.py sdist bdist_wheel"
   - On this step you might need to install build tools "pip3 install wheel setuptools"

3. Install package "pip3 install ."
   - If you wish to later uninstall "pip3 uninstall spotrpy"

4. Register an app in spotify for developers "https://developer.spotify.com/dashboard/applications"
   - Also set callback URI to "https://www.google.com/"

5. Run any spotr command
   - If command is not recognized, you might have to add wherever python stores packages to path, this can be different depending on OS.
       - <strong>Linux</strong> - on linux add "~/.local/bin" to your $PATH, this can be done by adding the following line to your .rc file (export PATH="$HOME/.local/bin:$PATH")
       - <strong>MacOs</strong> - on mac i personally fixed it by adding this to my .zshrc file (export PATH="$HOME/Library/Python/3.11/bin:$PATH") Here you have to change the python verion number accordingly

7. You will be prompted to create config.json and paste in client and secret id from spotify app

8. After these steps everything should work and you can enjoy spotr

</p>

<h1 align="center" style="border-bottom: none">Built-in Commands</h1>

<img align="center" width="100%" src="https://user-images.githubusercontent.com/58250866/228016178-f64c5866-4f84-4246-8c1f-97569baaf802.gif">


ascii       - Ascii image for current track <br>
authorise   - Authenticate with Spotify API <br>
config      - Modify config values in the terminal <br>
current     - Display information about the current track <br>
next        - Play next track <br>
playback    - Set playback state <br>
playlist    - Choose a playlist <br>
playlistadd - Add currently playing track to playlist <br>
previous    - Play previous track <br>
qsearch     - Quicksearch for tracks <br>
queue       - Get Queue <br>
recent      - Get recently played tracks <br>
recommend   - Play random / recommended tracks based on recent tracks <br>
refresh     - Refresh API key <br>
replay      - Replay/Restart currently playing song <br>
search      - Search for anything on spotify, Types - track, playlist, album <br>
seek        - Seek posistion for track in seconds <br>
shuffle     - Toggle shuffle, on / off <br>
start       - Start/Resume playing <br>
stop        - Stop/Pause playing <br>
vol         - Ajust volume <br>
volume      - Ajust volume <br>
web         - Open currently playing track in a broswer <br>

<h1 align="center" style="border-bottom: none">Debug mode</h1>
<p align="center">Simply change the debug variable in config.json file to enable debug mode (DEBUG="True")</p>

<img align="center" width="100%" src="https://user-images.githubusercontent.com/58250866/227784156-e1b56954-446b-4c13-9222-f82c4c71f5ce.gif">

<h1 align="center" style="border-bottom: none">Modifications</h1>
<p>

You can easily create your own commands and scripts by adding a function in router.py

As soon as the function is created and saved you can run it on the terminal with (spotr function-name)

<h4>I recommend going to spotifys <a href="https://developer.spotify.com/console/">API documentation</a> to get a grasp of what is possible</h4>
