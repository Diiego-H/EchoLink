import pytest
from models.song import SongInput
from crud.song import get_song_by_id, \
    get_songs_by_artist_id, \
    get_artist_by_song_id, \
    get_all_songs, create_song, \
    update_song, delete_song, \
    is_artist_owner_song, is_user_artist
from tests.utils import create_random_artist, create_random_song, get_session, create_random_listener
from fastapi import HTTPException
from models.user import RoleEnum

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
def test_get_song_by_id(db_session):

    artist = create_random_artist(db_session)
    song = create_random_song(db_session, artist.user.username)

    # Verify the song exists
    retrieved_song = get_song_by_id(db_session, song.song_id)
    assert retrieved_song is not None
    assert retrieved_song.song_id == song.song_id
    assert retrieved_song.title == song.title
    assert retrieved_song.album == song.album
    assert retrieved_song.genre == song.genre
    assert retrieved_song.release_date == song.release_date
    assert retrieved_song.artist_name == artist.user.username

    # Delete the song
    deleted_song = delete_song(db_session, retrieved_song.song_id)
    assert deleted_song.song_id == song.song_id

    # Verify the song no longer exists
    with pytest.raises(HTTPException) as exc_info:
        get_song_by_id(db_session, song.song_id)
    assert exc_info.value.status_code == 404

    # Clean up the artist
    db_session.delete(artist.user)
    db_session.commit()

# Test 2: Get songs by artist ID
def test_get_songs_by_artist_id(db_session):

    artist = create_random_artist(db_session)
    song1 = create_random_song(db_session, artist.user.username)
    song2 = create_random_song(db_session, artist.user.username)

    # Verify the songs exist
    retrieved_songs = get_songs_by_artist_id(db_session, artist.artist_id)
    assert len(retrieved_songs) == 2
    assert retrieved_songs[0].song_id == song1.song_id
    assert retrieved_songs[1].song_id == song2.song_id

    # Delete the songs
    deleted_song1 = delete_song(db_session, song1.song_id)
    assert deleted_song1.song_id == song1.song_id

    deleted_song2 = delete_song(db_session, song2.song_id)
    assert deleted_song2.song_id == song2.song_id

    # Verify the songs no longer exist
    retrieved_songs = get_songs_by_artist_id(db_session, artist.artist_id)
    assert len(retrieved_songs) == 0

    # Clean up the artist
    db_session.delete(artist.user)
    db_session.commit()

# Test 3: Get artist by song ID
def test_get_artist_by_song_id(db_session):

    artist = create_random_artist(db_session)
    song = create_random_song(db_session, artist.user.username)

    # Verify the artist exists
    retrieved_artist = get_artist_by_song_id(db_session, song.song_id)
    assert retrieved_artist is not None
    assert retrieved_artist.artist_id == artist.artist_id
    assert retrieved_artist.user.username == artist.user.username

    # Delete the song
    deleted_song = delete_song(db_session, song.song_id)
    assert deleted_song.song_id == song.song_id

    # Verify the artist no longer exists
    with pytest.raises(HTTPException) as exc_info:
        get_artist_by_song_id(db_session, song.song_id)
    assert exc_info.value.status_code == 404

    # Clean up the artist
    db_session.delete(artist.user)
    db_session.commit()

# Test 4: Get all songs
def test_get_all_songs(db_session):

    artist1 = create_random_artist(db_session)
    song1 = create_random_song(db_session, artist1.user.username)

    artist2 = create_random_artist(db_session)
    song2 = create_random_song(db_session, artist2.user.username)

    # Verify the songs exist
    retrieved_songs = get_all_songs(db_session)
    assert len(retrieved_songs) == 2
    assert retrieved_songs[0].song_id == song1.song_id
    assert retrieved_songs[1].song_id == song2.song_id

    # Delete the songs
    deleted_song1 = delete_song(db_session, song1.song_id)
    assert deleted_song1.song_id == song1.song_id

    deleted_song2 = delete_song(db_session, song2.song_id)
    assert deleted_song2.song_id == song2.song_id

    # Verify the songs no longer exist
    retrieved_songs = get_all_songs(db_session)
    assert len(retrieved_songs) == 0

    # Clean up the artists
    db_session.delete(artist1.user)
    db_session.delete(artist2.user)
    db_session.commit()

# Test 5: Create a song
def test_create_song(db_session):

    artist = create_random_artist(db_session)
    song_data = SongInput(
        title="Test Song",
        release_date="2021-01-01",
        album="Test Album",
        genre="Test Genre",
        artist_name=artist.user.username
    )

    # Create the song
    created_song = create_song(db_session, song_data)
    assert created_song is not None
    assert created_song.title == song_data.title
    assert created_song.album == song_data.album
    assert created_song.genre == song_data.genre
    assert created_song.release_date == song_data.release_date
    assert created_song.artist_name == artist.user.username

    # Verify the song exists
    retrieved_song = get_song_by_id(db_session, created_song.song_id)
    assert retrieved_song is not None
    assert retrieved_song.song_id == created_song.song_id
    assert retrieved_song.title == created_song.title
    assert retrieved_song.album == created_song.album
    assert retrieved_song.genre == created_song.genre
    assert retrieved_song.release_date == created_song.release_date
    assert retrieved_song.artist_name == created_song.artist_name

    # Delete the song
    deleted_song = delete_song(db_session, retrieved_song.song_id)
    assert deleted_song.song_id == retrieved_song.song_id

    # Verify the song no longer exists
    with pytest.raises(HTTPException) as exc_info:
        get_song_by_id(db_session, retrieved_song.song_id)
    assert exc_info.value.status_code == 404

    # Clean up the artist
    db_session.delete(artist.user)
    db_session.commit()

# Test 6: Update a song
def test_update_song(db_session):

    artist = create_random_artist(db_session)
    song = create_random_song(db_session, artist.user.username)

    song_data = SongInput(
        title="Updated Song",
        release_date="2022-01-01",
        album="Updated Album",
        genre="Updated Genre",
        artist_name=artist.user.username
    )

    # Update the song
    updated_song = update_song(db_session, song.song_id, song_data)
    assert updated_song is not None
    assert updated_song.song_id == song.song_id
    assert updated_song.title == song_data.title
    assert updated_song.album == song_data.album
    assert updated_song.genre == song_data.genre
    assert updated_song.release_date == song_data.release_date
    assert updated_song.artist_name == artist.user.username

    # Verify the song was updated
    retrieved_song = get_song_by_id(db_session, updated_song.song_id)
    assert retrieved_song is not None
    assert retrieved_song.song_id == updated_song.song_id
    assert retrieved_song.title == updated_song.title
    assert retrieved_song.album == updated_song.album
    assert retrieved_song.genre == updated_song.genre
    assert retrieved_song.release_date == updated_song.release_date
    assert retrieved_song.artist_name == updated_song.artist_name

    # Delete the song
    deleted_song = delete_song(db_session, retrieved_song.song_id)
    assert deleted_song.song_id == retrieved_song.song_id

    # Verify the song no longer exists
    with pytest.raises(HTTPException) as exc_info:
        get_song_by_id(db_session, retrieved_song.song_id)
    assert exc_info.value.status_code == 404

    # Clean up the artist
    db_session.delete(artist.user)
    db_session.commit()

# Test 7: Delete a song
def test_delete_song(db_session):

    artist = create_random_artist(db_session)
    song = create_random_song(db_session, artist.user.username)

    # Verify the song exists
    retrieved_song = get_song_by_id(db_session, song.song_id)
    assert retrieved_song is not None
    assert retrieved_song.song_id == song.song_id

    # Delete the song
    deleted_song = delete_song(db_session, retrieved_song.song_id)
    assert deleted_song.song_id == song.song_id

    # Verify the song no longer exists
    with pytest.raises(HTTPException) as exc_info:
        get_song_by_id(db_session, song.song_id)
    assert exc_info.value.status_code == 404

    # Clean up the artist
    db_session.delete(artist.user)
    db_session.commit()

# Check if an artist is the owner of a song
def test_is_artist_owner_song(db_session):

    artist = create_random_artist(db_session)
    artist2 = create_random_artist(db_session)
    song = create_random_song(db_session, artist.user.username)
    
    result = is_artist_owner_song(db_session, artist.artist_id, song.song_id)

    # Verify the artist is the owner of the song
    assert result is None

    # Verify the artist is not the owner of the song
    with pytest.raises(HTTPException) as exc_info:
        is_artist_owner_song(db_session, artist2.artist_id, song.song_id)
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "You are not the owner of this song"

    # Delete the song
    deleted_song = delete_song(db_session, song.song_id)
    assert deleted_song.song_id == song.song_id

    # Verify the song no longer exists
    with pytest.raises(HTTPException) as exc_info:
        is_artist_owner_song(db_session, artist.artist_id, song.song_id)
    assert exc_info.value.status_code == 404

    # Clean up the artist
    db_session.delete(artist.user)
    db_session.delete(artist2.user)
    db_session.commit()

# Check if a user is an artist
def test_is_user_artist(db_session):

    artist = create_random_artist(db_session)
    listener = create_random_listener(db_session)

    # Verify the user roles
    assert artist.user.role == RoleEnum.artist
    assert listener.user.role == RoleEnum.listener

    # Verify the user is an artist
    result_a = is_user_artist(db_session, artist.user.id)
    assert result_a is None

    # Verify the user is not an artist
    with pytest.raises(HTTPException) as exc_info:
        is_user_artist(db_session, listener.user.id)
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "You are not an artist"

    # Clean up the artist
    db_session.delete(artist.user)
    db_session.commit()

    # Clean up the listener
    db_session.delete(listener.user)
    db_session.commit()

