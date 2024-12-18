from fastapi.testclient import TestClient
from crud.playlist import create_playlist, add_song_to_playlist
from main import app
from core.config import get_db
from models.playlist import PlaylistInput, VisibilityEnum
from tests.utils import create_random_auth_user, create_random_song, create_random_artist

client = TestClient(app)

# Test for adding a song to a playlist
def test_add_song_to_playlist():
    db = next(get_db())

    # Create a random user
    user = create_random_auth_user(db)

    # Create a playlist for that user
    playlist_data = PlaylistInput(
        name="Add Song Playlist",
        description="Test add song",
        visibility=VisibilityEnum.public.value
    )
    playlist = create_playlist(db, playlist_data, user.id)

    artist = create_random_artist(db)
    song = create_random_song(db, artist.user.username)

    response = client.post(
        f"/playlist/{playlist.playlist_id}/song/{song.song_id}",
        headers={"Authorization": f"Bearer {user.token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert any(s["song_id"] == song.song_id for s in data["songs"])

    db.delete(playlist)
    db.delete(user)
    db.delete(artist.user)
    db.commit()

# Test for removing a song from a playlist
def test_remove_song_from_playlist():
    db = next(get_db())

    # Create a random user
    user = create_random_auth_user(db)

    # Create a playlist for that user
    playlist_data = PlaylistInput(
        name="Remove Song Playlist",
        description="Test remove song",
        visibility=VisibilityEnum.public.value
    )
    playlist = create_playlist(db, playlist_data, user.id)

    artist = create_random_artist(db)
    song = create_random_song(db, artist.user.username)

    playlist = add_song_to_playlist(db, playlist.playlist_id, song.song_id, user.id)

    response = client.delete(
        f"/playlist/{playlist.playlist_id}/song/{song.song_id}",
        headers={"Authorization": f"Bearer {user.token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert all(s["song_id"] != song.song_id for s in data["songs"])

    db.delete(playlist)
    db.delete(user)
    db.delete(artist.user)
    db.commit()

# Test for reordering songs in a playlist
def test_reorder_songs_in_playlist():
    db = next(get_db())

    # Create a random user
    user = create_random_auth_user(db)

    # Create a playlist for that user
    playlist_data = PlaylistInput(
        name="Reorder Playlist",
        description="Test reorder",
        visibility=VisibilityEnum.public.value
    )
    playlist = create_playlist(db, playlist_data, user.id)

    artist = create_random_artist(db)
    song1 = create_random_song(db, artist.user.username)
    song2 = create_random_song(db, artist.user.username)

    playlist = add_song_to_playlist(db, playlist.playlist_id, song1.song_id, user.id)
    playlist = add_song_to_playlist(db, playlist.playlist_id, song2.song_id, user.id)

    response = client.put(
        f"/playlist/{playlist.playlist_id}/reorder",
        json={"song_ids": [song2.song_id, song1.song_id]},
        headers={"Authorization": f"Bearer {user.token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["songs"][0]["song_id"] == song2.song_id
    assert data["songs"][1]["song_id"] == song1.song_id

    db.delete(playlist)
    db.delete(user)
    db.delete(artist.user)
    db.commit()
