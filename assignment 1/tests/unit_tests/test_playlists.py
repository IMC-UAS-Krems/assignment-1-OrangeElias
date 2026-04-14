from streaming.playlists import Playlist, CollaborativePlaylist
from streaming.tracks import Track
from streaming.users import FreeUser


class TestPlaylists:
    def test_owner_is_stored(self) -> None:
        owner = FreeUser("u1", "Owner", age=25)
        playlist = Playlist("p1", "Mix", owner=owner)
        assert playlist.owner is owner

    def test_add_track(self) -> None:
        owner = FreeUser("u1", "Owner", age=25)
        playlist = Playlist("p1", "Mix", owner=owner)
        track = Track("t1", "Song", 120, "pop")
        playlist.add_track(track)
        assert playlist.tracks == [track]

    def test_add_track_dedupes(self) -> None:
        owner = FreeUser("u1", "Owner", age=25)
        playlist = Playlist("p1", "Mix", owner=owner)
        track = Track("t1", "Song", 120, "pop")
        playlist.add_track(track)
        playlist.add_track(track)
        assert playlist.tracks == [track]

    def test_remove_track(self) -> None:
        owner = FreeUser("u1", "Owner", age=25)
        playlist = Playlist("p1", "Mix", owner=owner)
        track = Track("t1", "Song", 120, "pop")
        playlist.add_track(track)
        playlist.remove_track("t1")
        assert playlist.tracks == []

    def test_remove_track_noop_when_missing(self) -> None:
        owner = FreeUser("u1", "Owner", age=25)
        playlist = Playlist("p1", "Mix", owner=owner)
        track = Track("t1", "Song", 120, "pop")
        playlist.add_track(track)
        playlist.remove_track("missing")
        assert playlist.tracks == [track]

    def test_total_duration_seconds(self) -> None:
        owner = FreeUser("u1", "Owner", age=25)
        playlist = Playlist("p1", "Mix", owner=owner)
        t1 = Track("t1", "Song 1", 120, "pop")
        t2 = Track("t2", "Song 2", 150, "pop")
        playlist.add_track(t1)
        playlist.add_track(t2)
        assert playlist.total_duration_seconds() == 270

    def test_collaborative_starts_with_owner_contributor(self) -> None:
        owner = FreeUser("u1", "Owner", age=25)
        playlist = CollaborativePlaylist("p1", "Mix", owner=owner)
        assert playlist.contributors == [owner]

    def test_add_contributor(self) -> None:
        owner = FreeUser("u1", "Owner", age=25)
        user = FreeUser("u2", "Contributor", age=24)
        playlist = CollaborativePlaylist("p1", "Mix", owner=owner)
        playlist.add_contributor(user)
        assert user in playlist.contributors

    def test_add_contributor_dedupes(self) -> None:
        owner = FreeUser("u1", "Owner", age=25)
        user = FreeUser("u2", "Contributor", age=24)
        playlist = CollaborativePlaylist("p1", "Mix", owner=owner)
        playlist.add_contributor(user)
        playlist.add_contributor(user)
        assert playlist.contributors.count(user) == 1

    def test_remove_contributor_does_not_remove_owner(self) -> None:
        owner = FreeUser("u1", "Owner", age=25)
        playlist = CollaborativePlaylist("p1", "Mix", owner=owner)
        playlist.remove_contributor(owner)
        assert playlist.contributors == [owner]

    def test_remove_contributor_removes_non_owner(self) -> None:
        owner = FreeUser("u1", "Owner", age=25)
        user = FreeUser("u2", "Contributor", age=24)
        playlist = CollaborativePlaylist("p1", "Mix", owner=owner)
        playlist.add_contributor(user)
        playlist.remove_contributor(user)
        assert playlist.contributors == [owner]

    def test_collaborative_is_playlist(self) -> None:
        owner = FreeUser("u1", "Owner", age=25)
        playlist = CollaborativePlaylist("p1", "Mix", owner=owner)
        assert isinstance(playlist, Playlist)
