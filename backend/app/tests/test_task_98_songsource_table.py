from pydantic import ValidationError
import pytest
from models.song import SongInput
from crud.song import get_song_by_id, create_song, update_song, delete_song
from tests.utils import create_random_artist, create_random_song, get_session
from fastapi import HTTPException

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


# Test 1: Create a song with sources
def test_create_song_with_sources(db_session):
    artist = create_random_artist(db_session)
    song_data = SongInput(
        title="Test Song with Sources",
        release_date="2021-01-01",
        album="Test Album",
        genre="Test Genre",
        artist_name=artist.user.username,
        sources=["https://example.com/source1", "https://example.com/source2"]
    )

    # Create the song
    created_song = create_song(db_session, song_data)
    assert created_song is not None
    assert len(created_song.sources) == 2
    assert "https://example.com/source1" in created_song.sources
    assert "https://example.com/source2" in created_song.sources

    # Verify the song sources exist
    retrieved_song = get_song_by_id(db_session, created_song.song_id)
    assert retrieved_song is not None
    assert len(retrieved_song.sources) == 2
    assert "https://example.com/source1" in retrieved_song.sources
    assert "https://example.com/source2" in retrieved_song.sources

    # Clean up
    delete_song(db_session, retrieved_song.song_id)
    db_session.delete(artist.user)
    db_session.commit()


# Test 2: Update a song's sources
def test_update_song_sources(db_session):
    artist = create_random_artist(db_session)
    song = create_random_song(db_session, artist.user.username)

    song_data = SongInput(
        title="Updated Song with Sources",
        release_date="2022-01-01",
        album="Updated Album",
        genre="Updated Genre",
        artist_name=artist.user.username,
        sources=["https://newsource1.com/", "https://newsource2.com/"]
    )

    # Update the song
    updated_song = update_song(db_session, song.song_id, song_data)
    assert updated_song is not None
    assert len(updated_song.sources) == 2
    assert "https://newsource1.com/" in updated_song.sources
    assert "https://newsource2.com/" in updated_song.sources

    # Verify the song's sources were updated
    retrieved_song = get_song_by_id(db_session, updated_song.song_id)
    assert retrieved_song is not None
    assert len(retrieved_song.sources) == 2
    assert "https://newsource1.com/" in retrieved_song.sources
    assert "https://newsource2.com/" in retrieved_song.sources

    # Clean up
    delete_song(db_session, retrieved_song.song_id)
    db_session.delete(artist.user)
    db_session.commit()


# Test 3: Delete a song and ensure sources are deleted
def test_delete_song_with_sources(db_session):
    artist = create_random_artist(db_session)
    song_data = SongInput(
        title="Song with Sources to Delete",
        release_date="2021-01-01",
        album="Test Album",
        genre="Test Genre",
        artist_name=artist.user.username,
        sources=["https://delete-source1.com", "https://delete-source2.com"]
    )

    # Create the song
    created_song = create_song(db_session, song_data)
    assert created_song is not None

    # Verify the song and sources exist
    retrieved_song = get_song_by_id(db_session, created_song.song_id)
    assert retrieved_song is not None
    assert len(retrieved_song.sources) == 2

    # Delete the song
    deleted_song = delete_song(db_session, created_song.song_id)
    assert deleted_song is not None

    # Verify the song and its sources no longer exist
    with pytest.raises(HTTPException) as exc_info:
        get_song_by_id(db_session, created_song.song_id)
    assert exc_info.value.status_code == 404

    # Clean up
    db_session.delete(artist.user)
    db_session.commit()


# Test 4: Create a song without sources
def test_create_song_without_sources(db_session):
    artist = create_random_artist(db_session)
    song_data = SongInput(
        title="Song without Sources",
        release_date="2021-01-01",
        album="Test Album",
        genre="Test Genre",
        artist_name=artist.user.username,
        sources=[]
    )

    # Create the song
    created_song = create_song(db_session, song_data)
    assert created_song is not None
    assert len(created_song.sources) == 0

    # Verify the song exists without sources
    retrieved_song = get_song_by_id(db_session, created_song.song_id)
    assert retrieved_song is not None
    assert len(retrieved_song.sources) == 0

    # Clean up
    delete_song(db_session, retrieved_song.song_id)
    db_session.delete(artist.user)
    db_session.commit()


# Test 5: Input a song with invalid sources
def test_input_with_invalid_sources(db_session):
    artist = create_random_artist(db_session)

    # Verify that the input raises a ValidationError
    with pytest.raises(ValidationError):
        SongInput(
            title="Song with Invalid Sources",
            release_date="2023-01-01",
            album="Album Name",
            genre="Pop",
            artist_name=artist.user.username,
            sources=["not-a-url", "ftp://invalid-url"]
        )

    # Clean up
    db_session.delete(artist.user)
    db_session.commit()
