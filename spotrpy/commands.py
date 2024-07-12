from spotrpy.interface.Command import Command

from spotrpy.controllers.artistController import artistController
from spotrpy.controllers.previousController import previousController
from spotrpy.controllers.qsearchController import qsearchController
from spotrpy.controllers.queueController import queueController
from spotrpy.controllers.recentController import recentController
from spotrpy.controllers.recommendController import recommendController
from spotrpy.controllers.replayController import replayController
from spotrpy.controllers.searchController import searchController
from spotrpy.controllers.seekController import seekController
from spotrpy.controllers.shuffleController import shuffleController
from spotrpy.controllers.startController import startController
from spotrpy.controllers.stopController import stopController
from spotrpy.controllers.volumeController import volumeController
from spotrpy.controllers.webController import webController
from spotrpy.controllers.asciiController import asciiController
from spotrpy.controllers.nextController import nextController
from spotrpy.controllers.playbackController import playbackController
from spotrpy.controllers.playlistController import playlistController
from spotrpy.controllers.playlistaddController import playlistaddController
from spotrpy.controllers.authController import authController
from spotrpy.controllers.currentController import currentController

Command = Command()

"""
    Define all commands 

    Command.command takes following parameters:
    [
        'names': List -- name(s) / callword(s) for command,
        'description': str -- command description for argparser,
        'callable': Callable | List[Callable, 'metod'] -- callable to initialize / run on command execution (callable must accept 'args' parameter),
        'options': List *optional -- options passed to 'add_argument' function for command subparser (contains 'flags' and 'kwargs'),
    ]
"""

### AUTH 

Command.command(["auth", "authorize"], "Authorize Spotify api", [authController, "auth"], options=[
    {'flags': ['-ci', '--client_id'], 'kwargs': {'type': str, 'help': 'Your spotify-app client-id'}},
    {'flags': ['-cs', '--client_secret'], 'kwargs': {'type': str, 'help': 'Your spotify-app client-secret'}}
])

### TESTING

#Command.command(["hello"], "Terminal says hello", lambda args: print("hello!"))

#def world(args):
#    print("world!")
#Command.command(["world"], "function", world)

### SPOTR

Command.command(["artist"], "Display artist information", [artistController, "run"], options=[
    {'flags': ['artist'], 'kwargs': {'type': str, 'help': 'Optionally search for artist', 'nargs': '*'}}
])
Command.command(["ascii"], "Ascii image for current track", [asciiController, "run"], options=[
    {'flags': ['-w', '--width'], 'kwargs': {'type': str, 'help': 'Set ascii image width'}}
])
Command.command(["current"], "Display information about the currently playing track", [currentController, "run"])
Command.command(["next"], "Play next track", [nextController, "run"])
Command.command(["playback"], "Set playback state", [playbackController, "run"], options=[
    {'flags': ['-s', '--state'], 'kwargs': {'type': str, 'choices': ['track', 'context', 'off'], 'help': 'playback state'}}
])
Command.command(["playlist"], "Start playing one of your playlists", [playlistController, "run"])
Command.command(["playlistadd"], "Add currently playing track to a playlist", [playlistaddController, "run"])
Command.command(["previous"], "Play previous track", [previousController, "run"])
Command.command(["qsearch"], "Quicksearch for tracks", [qsearchController, "run"], options=[
    {'flags': ['query'], 'kwargs': {'type': str, 'help': 'Search query', 'nargs': '*'}}
])
Command.command(["queue"], "Display current queue", [queueController, "run"])
Command.command(["recent"], "Select one of recently played tracks", [recentController, "run"])
Command.command(["recommend"], "Play random / recommended tracks based on recent tracks", [recommendController, "run"])
Command.command(["replay"], "Replay/Restart currently playing track", [replayController, "run"])
Command.command(["search"], "Search for anything on spotify, Types - track, playlist, album", [searchController, "run"], options=[
    {'flags': ['query'], 'kwargs': {'type': str, 'help': 'Search query', 'nargs': '*'}},
    {'flags': ['-t', '--type'], 'kwargs': {'type': str, 'choices': ['track', 'playlist', 'album'], 'help': 'Search type'}}
])
Command.command(["seek"], "Seek posistion for track (in seconds)", [seekController, "run"], options=[
    {'flags': ['seconds'], 'kwargs': {'type': str, 'help': 'Song posistion'}},
])
Command.command(["shuffle"], "Toggle shuffle, on / off", [shuffleController, "run"], options=[
    {'flags': ['-s', '--state'], 'kwargs': {'type': str, 'choices': ['true', 'false'], 'help': 'Toggle shuffle'}}
])
Command.command(["start", "resume"], "Start/resume playing", [startController, "run"])
Command.command(["stop", "pause"], "Stop/Pause playing", [stopController, "run"])
Command.command(["volume", "vol"], "Ajust volume", [volumeController, "run"], options=[
    {'flags': ['-p', '--percentage'], 'kwargs': {'type': str, 'help': 'Volume percentage'}}
])
Command.command(["web"], "Open currently playing track in a broswer", [webController, "run"])

