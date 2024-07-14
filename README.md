
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

<img align="center" width="100%" src="https://github.com/user-attachments/assets/24094f70-4eae-4bd6-b0ae-06e5cab82c4a">

<h1 align="center" style="border-bottom: none">Debug</h1>

<img align="center" width="100%" src="https://github.com/user-attachments/assets/d53164f4-180d-4513-b2f1-0b34dd1f93bb">

<h1 align="center" style="border-bottom: none">Argparser</h1>

<img align="center" width="100%" src="https://github.com/Havard03/spotr/assets/58250866/c19ef190-7d01-4b78-9891-102efd9d61d7">

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

3. Run any spotr command (If command is not recognized check if python bin is in PATH)

4. You will be prompted to create config.json and paste in client and secret id from spotify app

5. After these steps everything should work and you can enjoy spotr

</p>

<h1 align="center" style="border-bottom: none">Built-in Commands</h1>

    auth                Authorize Spotify api
    authorize           Authorize Spotify api
    artist              Display artist information
    ascii               Ascii image for current track
    current             Display information about the currently playing track
    next                Play next track
    playback            Set playback state
    playlist            Start playing one of your playlists
    playlistadd         Add currently playing track to a playlist
    previous            Play previous track
    qsearch             Quicksearch for tracks
    queue               Display current queue
    recent              Select one of recently played tracks
    recommend           Play random / recommended tracks based on recent tracks
    replay              Replay/Restart currently playing track
    search              Search for anything on spotify, Types - track, playlist, album
    seek                Seek posistion for track (in seconds)
    shuffle             Toggle shuffle, on / off
    start               Start/resume playing
    resume              Start/resume playing
    stop                Stop/Pause playing
    pause               Stop/Pause playing
    volume              Ajust volume
    vol                 Ajust volume
    web                 Open currently playing track in a broswer

<h1 align="center" style="border-bottom: none">Modifications</h1>
<p>

Commands are declared in commands.py, Then you can set any function or class-method as callable.

<h4><a href="https://developer.spotify.com/documentation/web-api">API documentation</a></h4>

</p>


