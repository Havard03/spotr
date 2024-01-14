
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
A very simple CLI for controlling your spotify on the fly in the terminal. Made in python for simplicity
</p>

<img align="center" width="100%" src="https://github.com/Havard03/spotr/assets/58250866/1ab68044-f134-4a78-956a-7ac5641dae1f">

<h1 align="center" style="border-bottom: none">Installation</h1>

```
$ pip install spotrpy
```
Or clone the repo and install locally
```
$ pip install -e .
```

2. Register an app in spotify for developers "https://developer.spotify.com/dashboard/applications"
   - Also set callback URI to "https://www.google.com/"

3. Run any spotr command
   - If command is not recognized, you might have to add wherever python stores packages to path, this can be different depending on OS.
       - <strong>Linux</strong> - on linux add "~/.local/bin" to your $PATH, this can be done by adding the following line to your .rc file (export PATH="$HOME/.local/bin:$PATH")
       - <strong>MacOs</strong> - on mac i personally fixed it by adding this to my .zshrc file (export PATH="$HOME/Library/Python/3.11/bin:$PATH") Here you have to change the python verion number accordingly

4. You will be prompted to create config.json and paste in client and secret id from spotify app

5. After these steps everything should work and you can enjoy spotr

</p>

<h1 align="center" style="border-bottom: none">Built-in Commands</h1>

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

<h1 align="center" style="border-bottom: none">Modifications</h1>
<p>

You can easily create your own commands by adding a file in spotrpy/commands using the example.py template.
As soon as the file is created and saved you can run it on the terminal with (spotr command)

<h4>I recommend going to spotifys <a href="https://developer.spotify.com/console/">API documentation</a> to get a grasp of what is possible</h4>

</p>


