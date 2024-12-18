from sqlalchemy.orm import Session
from core.config import get_db
from crud.playlist import (
    create_playlist,
    add_song_to_playlist,
    remove_song_from_playlist,
    reorder_songs_in_playlist,
)
from models.playlist import PlaylistInput
from tests.utils import create_random_user, create_random_song, create_random_artist

# Test for adding a song to a playlist
def test_add_song_to_playlist():
    db: Session = next(get_db())

    # Create a random user and playlist
    user = create_random_user(db)
    playlist = create_playlist(
        db, 
        PlaylistInput(name="Test Playlist", description="Test Desc"), 
        user.id
    )

    # Create a random song
    artist = create_random_artist(db)
    song = create_random_song(db, artist.user.username)

    # Add song to playlist
    updated_playlist = add_song_to_playlist(db, playlist.playlist_id, song.song_id, user.id)

    # Verify the song is in the playlist
    assert updated_playlist is not None
    assert song.song_id in [s.song_id for s in updated_playlist.songs]

    # Cleanup
    db.delete(playlist)
    db.delete(user)
    db.delete(artist.user)
    db.commit()

# Test for removing a song from a playlist
def test_remove_song_from_playlist():
    db: Session = next(get_db())

    # Create a random user, playlist, and song
    user = create_random_user(db)
    playlist = create_playlist(
        db, 
        PlaylistInput(name="Test Playlist", description="Test Desc"), 
        user.id
    )
    artist = create_random_artist(db)
    song = create_random_song(db, artist.user.username)

    # Add song to playlist and then remove it
    add_song_to_playlist(db, playlist.playlist_id, song.song_id, user.id)
    updated_playlist = remove_song_from_playlist(db, playlist.playlist_id, song.song_id, user.id)

    # Verify the song is no longer in the playlist
    assert updated_playlist is not None
    assert song not in updated_playlist.songs

    # Cleanup
    db.delete(playlist)
    db.delete(user)
    db.delete(artist.user)
    db.commit()

# Test for reordering songs in a playlist
def test_reorder_songs_in_playlist():
    db: Session = next(get_db())

    # Create a random user and playlist
    user = create_random_user(db)
    playlist = create_playlist(
        db, 
        PlaylistInput(name="Test Playlist", description="Test Desc"), 
        user.id
    )

    # Create random songs and add to the playlist
    artist = create_random_artist(db)
    song1 = create_random_song(db, artist.user.username)
    song2 = create_random_song(db, artist.user.username)
    song3 = create_random_song(db, artist.user.username)
    add_song_to_playlist(db, playlist.playlist_id, song1.song_id, user.id)
    add_song_to_playlist(db, playlist.playlist_id, song2.song_id, user.id)
    add_song_to_playlist(db, playlist.playlist_id, song3.song_id, user.id)

    # Reorder songs
    new_order = [song3.song_id, song1.song_id, song2.song_id]
    reordered_playlist = reorder_songs_in_playlist(db, playlist.playlist_id, new_order, user.id)
    # Verify the new order
    reordered_song_ids = [song.song_id for song in reordered_playlist.songs]
    assert reordered_song_ids == new_order

    # Cleanup
    db.delete(playlist)
    db.delete(user)
    db.delete(artist.user)
    db.commit()

# Test for preventing duplicate songs in a playlist
def test_add_duplicate_song_to_playlist():
    db: Session = next(get_db())

    # Create a random user and playlist
    user = create_random_user(db)
    playlist = create_playlist(
        db, 
        PlaylistInput(name="Test Playlist", description="Test Desc"), 
        user.id
    )

    # Create a random song
    artist = create_random_artist(db)
    song = create_random_song(db, artist.user.username)

    # Add song to playlist twice
    add_song_to_playlist(db, playlist.playlist_id, song.song_id, user.id)
    try:
        add_song_to_playlist(db, playlist.playlist_id, song.song_id, user.id)
        assert False, "Expected ValueError for duplicate song, but it was not raised"
    except ValueError:
        pass  # Expected

    # Cleanup
    db.delete(playlist)
    db.delete(user)
    db.delete(artist.user)
    db.commit()

# Test for creating two playlists with the same name
def test_create_duplicate_playlist():
    db: Session = next(get_db())

    # Create a random user and playlist
    user = create_random_user(db)
    playlist = create_playlist(
        db, 
        PlaylistInput(name="Test Playlist", description="Test Desc"), 
        user.id
    )

    # Attempt to create a playlist with the same name
    try:
        create_playlist(db, PlaylistInput(name="Test Playlist", description="Test Desc"), user.id)
        assert False, "Expected ValueError for duplicate playlist, but it was not raised"
    except ValueError:
        pass  # Expected

    # Cleanup
    db.delete(playlist)
    db.delete(user)
    db.commit()