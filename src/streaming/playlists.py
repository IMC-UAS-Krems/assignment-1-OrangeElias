"""
playlists.py
------------
Implement playlist classes for organizing tracks.

Classes to implement:
  - Playlist
    - CollaborativePlaylist
"""
class Playlist:
    def __init__(self,playlist_id: str,name:str,owner):
        self.playlist_id=playlist_id
        self.name=name
        self.owner=owner
        self.tracks=[]
    def add_track(self,track):
        self.tracks.append(track)
    def remove_track(self,track_id):
        self.tracks = [track for track in self.tracks if track.track_id != track_id]
    def total_duration_seconds(self):
        return sum(track.duration_seconds for track in self.tracks)
    
class CollaborativePlaylist(Playlist):
    def __init__(self,playlist_id: str,name: str,owner):
        super().__init__(playlist_id,name,owner)
        self.contributers=[]
    def add_contributor(self,user):
        self.contributers.append(user)
    def remove_contributor(self,user):
        self.contributers.remove(user)