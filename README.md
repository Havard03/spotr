
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

<h3>Manual</h3>
</p>

Due to registration on pypi being temporarily disabled,you currently have to do a bit more manual work until it opens again

1. Clone repo to your computer and cd into folder

2. Build files "python3 setup.py sdist bdist_wheel"

3. Install package "pip3 install ." (if you wish to later uninstall "pip3 uninstall spotrpy")

4. Register an app in spotify for developers "https://developer.spotify.com/dashboard/applications" (also set callback URI to "https://www.google.com/")

5. Run any spotr command

6. You will be prompted to create config.json and paste in client and secret id from spotify app

7. After these steps everything should work and you can enjoy spotr

</p>

<h1 align="center" style="border-bottom: none">Built-in Commands</h1>

<img align="center" width="100%" src="https://user-images.githubusercontent.com/58250866/228016178-f64c5866-4f84-4246-8c1f-97569baaf802.gif">


ascii       - Ascii image for current track
authorise   - Authenticate with Spotify API
config      - Modify config values in the terminal
current     - Display information about the current track
next        - Play next track
playback    - Set playback state
playlist    - Choose a playlist
playlistadd - Add currently playing track to playlist
previous    - Play previous track
qsearch     - Quicksearch for tracks
queue       - Get Queue
recent      - Get recently played tracks
recommend   - Play random / recommended tracks based on recent tracks
refresh     - Refresh API key
replay      - Replay/Restart currently playing song
search      - Search for anything on spotify, Types - track, playlist, album
seek        - Seek posistion for track in seconds
shuffle     - Toggle shuffle, on / off
start       - Start/Resume playing
stop        - Stop/Pause playing
vol         - Ajust volume
volume      - Ajust volume
web         - Open currently playing track in a broswer

<h1 align="center" style="border-bottom: none">Debug mode</h1>
<p align="center">Simply change the debug variable in .env file to enable debug mode (DEBUG="True")</p>

<img align="center" width="100%" src="https://user-images.githubusercontent.com/58250866/227784156-e1b56954-446b-4c13-9222-f82c4c71f5ce.gif">

<h1 align="center" style="border-bottom: none">Modifications</h1>
<p>

You can easily create your own commands and scripts by adding a function in router.py

As soon as the function is created and saved you can run it on the terminal with (spotr function-name)

<h4>I recommend going to spotifys <a href="https://developer.spotify.com/console/">API documentation</a> to get a grasp of what is possible</h4>

</p>


