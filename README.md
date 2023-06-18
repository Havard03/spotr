
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

<h1 align="center" style="border-bottom: none">Installation</h1>

<h3>Script</h3>
<p>

1. Got to <a href="https://developer.spotify.com/dashboard/">Spotify dashboard</a> and register an app

2. In options, set callback URI to "https://www.google.com/"

3. Clone repo, cd into folder, and run install script (python3 install.py)

4. Follow instructions in script

5. Run spotr in terminal and enjoy

</p>

<h3>Manual</h3>
</p>

1. Clone repo to your computer and cd into folder

2. Make .spotr file executable "chmod u+x spotr"

3. Register an app in spotify for developers "https://developer.spotify.com/dashboard/applications" (also set callback URI to "https://www.google.com/")

4. Install project requirements: pip3 install -r requirements.txt

5. Run "spotr authorise" command in terminal and enter keys from the registered spotify app

6. Follow the steps and check that all relevant data was written to .env file

7. Add current folder to PATH so the spotr file is excecutable everywhere

9. Run spotr in terminal and enjoy

</p>

<h1 align="center" style="border-bottom: none">Built-in Commands</h1>

<img align="center" width="100%" src="https://user-images.githubusercontent.com/58250866/228016178-f64c5866-4f84-4246-8c1f-97569baaf802.gif">

<h2>Main commands</h2>

<h3>Single argument</h3>
Current     - Displays info for the currently playing song <br> 
Web         - Open currently playing song in a browser <br>
Queue       - Get a list over song in your current queue <br>
Next        - Play next song <br>
Previous    - Play previous song <br>
Start       - Start playing <br>
Stop        - Stop / Pause playing <br>
Replay      - Replay / Restart currently playing song <br>
Recent      - Get a list of your recently played songs <br>
Volume      - Set volume in precentage <br>
Shuffle     - Toggle shuffle on or off <br>
Seek        - Seek track posistion in seconds <br>
Playlist    - Start playing one of your playlists <br>
Playlistadd - Add currently playing song to one of your playlists <br>
Playback    - Set playback state <br>
Suprise     - Play recommended song based on recently played tracks<br>

<h3>Requires second argument</h3>
Search      - Search for a song on spotify <br>
Album       - Search for albums on spotify <br>

<h2>Other</h2>
Refresh     - Manually refresh spotify api token <br>
Authorise   - Manually start authorisation processs <br>

<h1 align="center" style="border-bottom: none">Debug mode</h1>
<p align="center">Simply change the debug variable in .env file to enable debug mode (DEBUG="True")</p>

<img align="center" width="100%" src="https://user-images.githubusercontent.com/58250866/227784156-e1b56954-446b-4c13-9222-f82c4c71f5ce.gif">

<h1 align="center" style="border-bottom: none">Modifications</h1>
<p>

You can easily create your own commands and scripts by adding a function in router.py

As soon as the function is created and saved you can run it on the terminal with (spotr function-name)

<h4>I recommend going to spotifys <a href="https://developer.spotify.com/console/">API documentation</a> to get a grasp of what is possible</h4>

</p>


