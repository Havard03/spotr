from rich.console import Console

console = Console()

class Helpers():
    
    def parseTracks(self, data, key="track"):
        
        choices=[]
        longest_track = "" 
        
        if (not key == None):     
            for track in data:
                if len(track[key]['name']) > len(longest_track):
                    longest_track = track[key]['name']
            for track in data:
                artist_names = ', '.join([artist['name'] for artist in track[key]['artists']])
                choices.append("{0:<{track_width}} -- {1}".format(track[key]['name'], artist_names, track_width=len(longest_track)))
        else:
            for track in data:
                if len(track['name']) > len(longest_track):
                    longest_track = track['name']
            for track in data:
                artist_names = ', '.join([artist['name'] for artist in track['artists']])
                choices.append("{0:<{track_width}} -- {1}".format(track['name'], artist_names, track_width=len(longest_track)))
        
        choices = dict.fromkeys(choices)
        choices = list(filter(None, choices))
        
        return choices
        
    
    def parseAlbums(self, data):
        choices=[]
        for playlist in data: choices.append(playlist['name'])
        choices = dict.fromkeys(choices) 
        choices = list(filter(None, choices))
        
        return choices