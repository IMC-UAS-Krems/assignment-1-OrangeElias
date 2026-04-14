"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""
from datetime import datetime, timedelta

from .users import PremiumUser


class StreamingPlatform:
    def __init__(self,name:str):
        self._name=name
        self._catalogue={}
        self._users={}
        self._artists={}
        self._albums={}
        self._playlists={}
        self._sessions=[]
    def add_track(self,track):
         self._catalogue[track.track_id]=track
    def add_user(self,user):
         self._users[user.user_id]=user
    def add_artist(self,artist):
          self._artists[artist.artist_id]=artist
    def add_album(self,album):
          self._albums[album.album_id]=album
    def add_playlist(self,playlist):
         self._playlists[playlist.playlist_id]=playlist
    def record_session(self,session):
      self._sessions.append(session)
    def get_track(self,track_id):
       try:
        return self._catalogue[track_id]
       except:
          return "None"
    def get_user(self,user_id):
       try:
        return self._users[user_id]
       except:
          return "None"
    def get_artist(self,artist_id):
       try:
        return self._artists[artist_id]
       except:
          return "None"
    def get_album(self,album_id):
       try:
          return self._albums[album_id]
       except:
          return "None"
    def all_users(self):
        return list(self._users.values())
    def all_tracks(self):
       return list(self._catalogue.values())
    def total_listening_time_minutes(self,start, end):
      total_seconds = sum(
         session.duration_listened_seconds
         for session in self._sessions
         if start <= session.timestamp <= end
      )
      return total_seconds / 60.0
    def avg_unique_tracks_per_premium_user(self,days:int=30):
      premium_users = []
      for user in self._users.values():
         if isinstance(user, PremiumUser):
            premium_users.append(user)
      if len(premium_users) == 0:
         return 0.0
      cutoff = datetime.now() - timedelta(days=days)
      total = 0
      for user in premium_users:
         ids = set()
         for session in user.sessions:
            if session.timestamp >= cutoff:
               ids.add(session.track.track_id)
         total += len(ids)
      return total / len(premium_users)

