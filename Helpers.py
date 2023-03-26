""" Helper Class """

from rich.console import Console

console = Console()


class Helpers:
    """Helper functions for Router"""

    def parse_tracks(self, data, key=None):
        """Parse tracks for questionary"""
        choices = []
        longest_track = ""
        for track in data:
            if len(track["name"] if not key else track["track"]["name"]) > len(
                longest_track
            ):
                longest_track = track["name"] if not key else track["track"]["name"]
        for track in data:
            artist_names = ", ".join(
                [
                    artist["name"]
                    for artist in (
                        track["artists"] if not key else track["track"]["artists"]
                    )
                ]
            )
            choices.append(
                "{0:<{track_width}} -- {1}".format(
                    (track["name"] if not key else track["track"]["name"]),
                    artist_names,
                    track_width=len(longest_track),
                )
            )

        choices = dict.fromkeys(choices)
        choices = list(filter(None, choices))

        return choices

    def parse_albums(self, data):
        """Parse albums for questionary"""
        choices = []
        for playlist in data:
            choices.append(playlist["name"])
        choices = dict.fromkeys(choices)
        choices = list(filter(None, choices))

        return choices
