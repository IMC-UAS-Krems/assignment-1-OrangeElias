"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""
from streaming.tracks import Song, AlbumTrack
from streaming.playlists import CollaborativePlaylist
from streaming.users import PremiumUser, FamilyAccountUser, FamilyMember


from datetime import datetime, timedelta
from typing import TYPE_CHECKING
from .users import PremiumUser
from statistics import mean
from datetime import datetime, timezone, timedelta
from itertools import groupby, islice

class StreamingPlatform:
   def __init__(self,name:str):
      #assigns all attributes
        self._name=name
        self._catalogue={}
        self._users={}
        self._artists={}
        self._albums={}
        self._playlists={}
        self._sessions=[]
    
   def add_track(self,track):
      #adds track  
      self._catalogue[track.track_id]=track
    
   def add_user(self,user):
      #adds user
      self._users[user.user_id]=user
    
   def add_artist(self,artist):
      #adds artist
      self._artists[artist.artist_id]=artist
    
   def add_album(self,album):
      #adds album
      self._albums[album.album_id]=album
    
   def add_playlist(self,playlist):
      #adds playlist
      self._playlists[playlist.playlist_id]=playlist
    
   def record_session(self,session):
      #adds session
      self._sessions.append(session)
   
   def get_track(self,track_id):
      #gets track from dic with track_id as key
      return self._catalogue[track_id]
      
   def get_user(self,user_id):
      #get user from dic with user_id as key
      return self._users[user_id]
       
   def get_artist(self,artist_id):
      #get artist from dic with artist_id as key
      return self._artists[artist_id]
   
   def get_album(self,album_id):
      #get album from dic with ablum_id as key
      return self._albums[album_id]
          
   def all_users(self):
      #returns list of all users  
      return list(self._users.values())
    
   def all_tracks(self):
      #Gets all tracks
      return list(self._catalogue.values())
    
   def total_listening_time_minutes(self,start, end):
      #takes parameters of when session started and ended
      total_seconds = sum(                                  #sum function adds the seconds together
         session.duration_listened_seconds                  #takes from session the listened seconds
         for session in self._sessions                      #loops through all sessions
         if start <= session.timestamp <= end               #checks if its in the time frame
      )
      return total_seconds / 60.0                           #returns the minutes
    
   def avg_unique_tracks_per_premium_user(self,days:int=30):
      premium_users = []
      total = 0
      for user in self._users.values():
         if isinstance(user, PremiumUser):                  #checks if premium user
            premium_users.append(user)                      #adds to list if premium user
      if len(premium_users) == 0:
         return 0.0
      cutoff = datetime.now() - timedelta(days=days)        #makes sure its the last 30 days
      for user in premium_users:                            #loops through the created list
         track_ids = set()                                  #makes a set, so no track_id comes twice
         for session in user.sessions:                      #loops through sessions
            if session.timestamp >= cutoff:                 #checks if the timestamp is last 30 days
               track_ids.add(session.track.track_id)        #adds every track id to the set
         total += len(track_ids)                            #gets how many tracks in total of all premium users
      return total / len(premium_users)                     #returns the average track per listener
    
   def track_with_most_distinct_listeners(self):
      if not self._sessions:                                #checks, if there are even sessions
         return None
      track_users = {}
      for session in self._sessions:                        #loops throughs sessions
         track_id = session.track.track_id                  #gets the id of track
         user_id = session.user.user_id                     #gets id of user
         if track_id not in track_users:                    #checks if track is already in dic
               track_users[track_id] = set()                #adds the id with a set (so no double users)
         track_users[track_id].add(user_id)                 #adds user listener to the track
      most_listened_track_id = max(track_users, key=lambda t: len(track_users[t])) #gets with max function and lambda the track id with the most listeners
      for session in self._sessions:                        #loops through sessions
         if session.track.track_id == most_listened_track_id: #searches for the name of the track id
               return session.track                         #returns the name of the most listened track
   
   def avg_session_duration_by_user_type(self):
      data = {}
      result = []
      for session in self._sessions:                         #loops through sessions
         user_type = session.user.__class__.__name__         #gets the user type of this one session
         if user_type not in data:                           #if the user_type not in data, then it gets added into the data dic with a list for the users listening time
               data[user_type] = []
         data[user_type].append(session.duration_seconds)    #the duration seconds gets appended into the list
      for user_type, durations in data.items():               #loops through the lists of the user_types
         average_listening_time = sum(durations) / len(durations)#gets the average_listening_time per user_type
         result.append((user_type, average_listening_time))  #results get appended into the list per user type as tuple
      return sorted(result, key=lambda x: x[1], reverse=True) #returns list of sorted longest average_listening_time to shortest

   def total_listening_time_underage_sub_users_minutes(self, age: int = 18):
      total_seconds = 0
      for session in self._sessions:                          #loops throughs sessions
        if isinstance(session.user, FamilyMember) and session.user.age < age: #checjs if user is family member and underage
            total_seconds += session.duration_listened_seconds #adds listened seconds to total_seconds
      return total_seconds / 60  #returns in minutes
   
   def top_artists_by_listening_time(self,n: int = 5):
      artist_time = {}                                      #create dic for all artists
      for session in self._sessions:                        
        if isinstance(session.track, Song):                 #checks if the track is a song and nothing different
            artist = session.artist                         #declares the artist of the session
            artist_time[artist] = artist_time.get(artist) + session.duration_listened_seconds #adds the listened time of the session to the listened time of the artist in the dic
      sorted_artists = sorted(artist_time.items(), key=lambda x: x[1], reverse=True) #sorts the artists, so that the highest listened to is first
      all_top_artists=[(artist, total / 60.0) for artist, total in sorted_artists[:n]] #uses parameter n(default=5) to get top n listened to artists
      return all_top_artists

   def user_top_genre(self,user_id: str):
      genre_time={}
      total_time=0
      if user_id not in self._users:                        #checks, if user exists
         return None
      for session in self._sessions:
         if session.user.user_id == user_id:                 #gets the sessions of the user
            genre = session.track.genre                     #detects the genere of the track
            genre_time[genre] = genre_time.get(genre) + session.duration_listened_seconds #adds per genre extra listening time of the track
            total_time+=session.duration_listened_seconds
      if not genre_time:                                    #checks if there is even time listened to the genre
         return None
      top_genre = max(genre_time.items(), key=lambda x: x[1])[0]  #uses max function to get the name of the top genre
      top_genre_time = genre_time[top_genre]                #gets the time of the top genre
      percentage = (top_genre_time / total_time) * 100      #calculates the percentage listened to
      result=(top_genre,percentage)                         #result becomes a tuple
      return result
   
   def collaborative_playlists_with_many_artists(self, threshold: int = 3):
    result = []
    for playlist in self._playlists.values():               #loops through all playlists
        if not isinstance(playlist, CollaborativePlaylist): #checks if its a CollaborativePlaylist
            continue
        artist_ids = {                                      #makes with a loop a set of artist ids
            track.artist.artist_id                          #takes the trackid of the song
            for track in playlist.tracks
            if isinstance(track, Song)                      #takes only tracks with attribute song
        }
        if len(artist_ids) > threshold:                     #if the playlist has more than 3 artists, then it gets added to the result
            result.append(playlist)
    return result
   
   def avg_tracks_per_playlist_type(self):
      data = {}                                             #dic for later
      playlist_count = 0                                    #all the counts to get an average
      playlist_tracks = 0
      collab_count = 0
      collab_tracks = 0
      for playlist in self._playlists.values():             #loops through playlist
        if isinstance(playlist, CollaborativePlaylist):     #checks if its CollaborativePlaylist else its a normal playlist
            collab_count += 1
            collab_tracks += len(playlist.tracks)           #length of tracks added for the avarage later
        else:
            playlist_count += 1
            playlist_tracks += len(playlist.tracks)
      data["Playlist"] = (
        playlist_tracks / playlist_count if playlist_count > 0 else 0.0 #makes the average or else makes the average 0.0
      ) 
      data["CollaborativePlaylist"] = (
        collab_tracks / collab_count if collab_count > 0 else 0.0
      )
      return data

   def users_who_completed_albums(self):
    result = []

      # gehe jeden User durch
    for user in self._users.values():

         # sammle alle Track-IDs, die der User gehört hat
         listened_tracks = set()
      for session in user.sessions:
               listened_tracks.add(session.track.track_id)

         completed_albums = []

         # gehe alle Alben durch
         for album in self._albums.values():

               # überspringe leere Alben
               if len(album.tracks) == 0:
                  continue

               all_tracks_listened = True

               # prüfe jeden Track im Album
               for track in album.tracks:
                  if track.track_id not in listened_tracks:
                     all_tracks_listened = False
                     break

               # wenn alle Tracks gehört wurden → Album hinzufügen
               if all_tracks_listened:
                  completed_albums.append(album.title)

         # nur User hinzufügen, die mindestens ein Album fertig gehört haben
         if len(completed_albums) > 0:
               result.append((user, completed_albums))

      return result
        
           
      