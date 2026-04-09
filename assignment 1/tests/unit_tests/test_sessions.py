from datetime import datetime

from streaming.sessions import ListeningSession
from streaming.users import FreeUser
from streaming.tracks import Track


class TestSessions:
    def test_stores_user_and_track(self) -> None:
        user = FreeUser("u1", "User", age=20)
        track = Track("t1", "Track", 120, "pop")
        session = ListeningSession("s1", user, track, datetime(2024, 1, 1), 120)
        assert session.user is user
        assert session.track is track

    def test_duration_listened_minutes(self) -> None:
        user = FreeUser("u1", "User", age=20)
        track = Track("t1", "Track", 120, "pop")
        session = ListeningSession("s1", user, track, datetime(2024, 1, 1), 120)
        assert session.duration_listened_minutes() == 2.0

    def test_timestamp_stored(self) -> None:
        user = FreeUser("u1", "User", age=20)
        track = Track("t1", "Track", 120, "pop")
        ts = datetime(2024, 1, 1)
        session = ListeningSession("s1", user, track, ts, 120)
        assert session.timestamp is ts

    def test_duration_seconds_stored(self) -> None:
        user = FreeUser("u1", "User", age=20)
        track = Track("t1", "Track", 120, "pop")
        session = ListeningSession("s1", user, track, datetime(2024, 1, 1), 90)
        assert session.duration_listened_seconds == 90

