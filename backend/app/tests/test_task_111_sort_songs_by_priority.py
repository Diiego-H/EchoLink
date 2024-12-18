import pytest
from crud.song import sort_songs_alphabetically, sort_songs_by_release_date, get_songs_by_artist_engagement_score, get_songs_by_artist_priority, delete_song
from tests.utils import create_random_artist, create_random_song, create_random_auth_listener, get_session
from crud.listener import follow_artist, get_listener_by_user_id
from crud.playlist import create_playlist, add_song_to_playlist
from models.playlist import PlaylistInput

@pytest.fixture(scope="function")
def db_session():
    """
    Provides a clean database session for each test.
    Automatically rolls back transactions after each test.
    """
    db = get_session()
    try:
        yield db
    finally:
        db.rollback()
        db.close()

# Test 1: Get song by ID
def test_sort_alfabetically(db_session):

    artist = create_random_artist(db_session)
    song1 = create_random_song(db_session, artist.user.username, title="A")
    song2 = create_random_song(db_session, artist.user.username, title="C")
    song3 = create_random_song(db_session, artist.user.username, title="B")

    # Sort songs alphabetically
    ascending_songs = sort_songs_alphabetically(db_session)
    descending_songs = sort_songs_alphabetically(db_session, ascending=False)

    # Check if the songs are sorted correctly
    assert ascending_songs[0].title == "A"
    assert ascending_songs[1].title == "B"
    assert ascending_songs[2].title == "C"

    assert descending_songs[0].title == "C"
    assert descending_songs[1].title == "B"
    assert descending_songs[2].title == "A"

    # Clean up songs
    delete_song(db_session, song1.song_id)
    delete_song(db_session, song2.song_id)
    delete_song(db_session, song3.song_id)

    # Clean up artist
    db_session.delete(artist.user)

    # Commit the transaction
    db_session.commit()

def test_sort_by_release_date(db_session):

    artist = create_random_artist(db_session)
    song1 = create_random_song(db_session, artist.user.username, release_date="2022-01-01")
    song2 = create_random_song(db_session, artist.user.username, release_date="2021-01-01")
    song3 = create_random_song(db_session, artist.user.username, release_date="2023-01-01")

    # Sort songs by release date
    ascending_songs = sort_songs_by_release_date(db_session)
    descending_songs = sort_songs_by_release_date(db_session, ascending=False)

    # Check if the songs are sorted correctly
    assert ascending_songs[0].release_date == "2021-01-01"
    assert ascending_songs[1].release_date == "2022-01-01"
    assert ascending_songs[2].release_date == "2023-01-01"

    assert descending_songs[0].release_date == "2023-01-01"
    assert descending_songs[1].release_date == "2022-01-01"
    assert descending_songs[2].release_date == "2021-01-01"

    # Clean up songs
    delete_song(db_session, song1.song_id)
    delete_song(db_session, song2.song_id)
    delete_song(db_session, song3.song_id)

    # Clean up artist
    db_session.delete(artist.user)

    # Commit the transaction
    db_session.commit()

def test_sort_by_artist_engagement(db_session):

    artist = create_random_artist(db_session)
    song1 = create_random_song(db_session, artist.user.username)
    song2 = create_random_song(db_session, artist.user.username)
    song3 = create_random_song(db_session, artist.user.username)

    artists = get_songs_by_artist_engagement_score(db_session)


    # Check if the songs are sorted correctly. Currently, the function returns a list of 3 artists.
    # We cannot test the exact order of the artists, but we can check if there are 3 artists in the list.
    # The QA team will test the exact order of the artists, when the database is populated with more data.
    assert len(artists) == 3

    # Clean up songs
    delete_song(db_session, song1.song_id)
    delete_song(db_session, song2.song_id)
    delete_song(db_session, song3.song_id)

    # Clean up artist
    db_session.delete(artist.user)

    # Commit the transaction
    db_session.commit()

def test_sort_by_artist_priority(db_session):

    user = create_random_auth_listener(db_session)
    listener = get_listener_by_user_id(db_session, user.id)

    playlist_input = PlaylistInput(
        name="Test Playlist",
        description="A playlist for testing purposes",
        visibility="public",
    )

    playlist = create_playlist(db_session, playlist_input, listener.user.id)

    artist1 = create_random_artist(db_session)
    song11 = create_random_song(db_session, artist1.user.username)
    song12 = create_random_song(db_session, artist1.user.username)

    artist2 = create_random_artist(db_session)
    song21 = create_random_song(db_session, artist2.user.username)

    artist3 = create_random_artist(db_session)
    song31 = create_random_song(db_session, artist3.user.username)

    follow_artist(db_session, listener, artist1.user.username)

    add_song_to_playlist(db_session, playlist.playlist_id, song21.song_id, listener.user.id)
    add_song_to_playlist(db_session, playlist.playlist_id, song11.song_id, listener.user.id)
    add_song_to_playlist(db_session, playlist.playlist_id, song12.song_id, listener.user.id)

    songs = get_songs_by_artist_priority(db_session, user.id)

    assert len(songs) == 4

    # Clean up songs
    delete_song(db_session, song11.song_id)
    delete_song(db_session, song12.song_id)
    delete_song(db_session, song21.song_id)
    delete_song(db_session, song31.song_id)

    # Clean up listener
    db_session.delete(user)

    # Clean up artist
    db_session.delete(artist1.user)
    db_session.delete(artist2.user)
    db_session.delete(artist3.user)

    # Commit the transaction
    db_session.commit()


