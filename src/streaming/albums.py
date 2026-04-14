"""
albums.py
---------
Implement the Album class for collections of AlbumTrack objects.

Classes to implement:
  - Album
"""
from . import tracks

class Album:
    def __init__(self, album_id: str, title: str, artist: str, release_year: int):
        self.album_id = album_id
        self.title = title
        self.artist = artist
        self.release_year = release_year
        self.tracks = []
   
    def add_track(self, track):
        # Set the album reference on the track
        track.album = self
        # Add the track
        self.tracks.append(track)
        # Keep tracks sorted by track_number
        self.tracks.sort(key=lambda t: t.track_number)

    def track_ids(self):
        return {track.track_id for track in self.tracks}

    def duration_seconds(self):
        return sum(track.duration_seconds for track in self.tracks)
