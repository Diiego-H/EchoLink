from fastapi import HTTPException
import pytest
from models.user import ListenerArtistLink
from crud.listener import follow_artist, unfollow_artist
from tests.utils import create_listener, create_artist, get_session

@pytest.fixture(scope="function")
def db_session():
    """
    Provides a clean database session for each test.
    Automatically rolls back transactions after each test.
    """
    db = get_session()  # Assume get_session() provides a valid SQLAlchemy session
    try:
        yield db
    finally:
        db.rollback()
        db.close()


def test_follow_artist_success(db_session):
    # Arrange: Create listener and artist
    listener = create_listener(db_session)
    artist = create_artist(db_session)

    # Act: Follow the artist
    follow_link = follow_artist(db_session, listener, artist.user.username)

    # Assert: Check that the follow relationship was created
    assert follow_link.listener_id == listener.listener_id
    assert follow_link.artist_id == artist.artist_id

    # Verify database entries
    db_follow = db_session.query(ListenerArtistLink).filter_by(listener_id=listener.listener_id, artist_id=artist.artist_id).first()
    assert db_follow is not None

    # Cleanup
    db_session.delete(listener.user)
    db_session.delete(artist.user)
    db_session.commit()


def test_follow_artist_already_following(db_session):
    # Arrange: Create listener and artist
    listener = create_listener(db_session)
    artist = create_artist(db_session)

    # Create an existing follow relationship
    follow_link = ListenerArtistLink(listener_id=listener.listener_id, artist_id=artist.artist_id)
    db_session.add(follow_link)
    db_session.commit()

    # Act & Assert: Check that HTTPException is raised when trying to follow again
    with pytest.raises(HTTPException) as exc_info:
        follow_artist(db_session, listener, artist.user.username)
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "The listener follows the artist."

    # Cleanup
    db_session.delete(listener.user)
    db_session.delete(artist.user)
    db_session.commit()


def test_follow_artist_nonexistent_artist(db_session):
    # Arrange: Create listener
    listener = create_listener(db_session)

    # Act & Assert: Check that HTTPException is raised when artist doesn't exist
    with pytest.raises(HTTPException) as exc_info:
        follow_artist(db_session, listener, "non_existent_artist")
    
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found."

    # Cleanup
    db_session.delete(listener.user)
    db_session.commit()


def test_unfollow_artist_success(db_session):
    # Arrange: Create listener and artist
    listener = create_listener(db_session)
    artist = create_artist(db_session)

    # Create an existing follow relationship
    follow_link = ListenerArtistLink(listener_id=listener.listener_id, artist_id=artist.artist_id)
    db_session.add(follow_link)
    db_session.commit()

    # Act: Unfollow the artist
    unfollow_artist(db_session, listener, artist.user.username)

    # Assert: Verify the follow relationship no longer exists in the database
    db_follow = db_session.query(ListenerArtistLink).filter_by(listener_id=listener.listener_id, artist_id=artist.artist_id).first()
    assert db_follow is None

    # Cleanup
    db_session.delete(listener.user)
    db_session.delete(artist.user)
    db_session.commit()


def test_unfollow_artist_not_following(db_session):
    # Arrange: Create listener and artist
    listener = create_listener(db_session)
    artist = create_artist(db_session)

    # Act & Assert: Ensure HTTPException is raised when trying to unfollow an artist not followed
    with pytest.raises(HTTPException) as exc_info:
        unfollow_artist(db_session, listener, artist.user.username)
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "The listener does not follow the artist."

    # Cleanup
    db_session.delete(listener.user)
    db_session.delete(artist.user)
    db_session.commit()


def test_unfollow_artist_nonexistent_artist(db_session):
    # Arrange: Create listener
    listener = create_listener(db_session)

    # Act & Assert: Ensure HTTPException is raised when the artist does not exist
    with pytest.raises(HTTPException) as exc_info:
        unfollow_artist(db_session, listener, "non_existent_artist")
    
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found."

    # Cleanup
    db_session.delete(listener.user)
    db_session.commit()
