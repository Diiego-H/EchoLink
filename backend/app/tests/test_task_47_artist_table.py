import pytest
from tests.utils import create_random_user, get_session
from crud.artist import get_artist_by_user_id, create_artist, get_artist_by_username
from models.artist import Artist

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
        # Cleanup: Rollback any changes made during the test
        db.rollback()
        db.close()

# Test: Get artist by user_id
def test_get_artist_by_user_id(db_session):
    user = create_random_user(db_session)
    artist = Artist(user_id=user.id, name="Test Artist", genre="Test Genre", bio="Test Bio")
    db_session.add(artist)
    db_session.commit()
    db_session.refresh(artist)

    retrieved_artist = get_artist_by_user_id(db_session, user.id)
    assert retrieved_artist is not None
    assert retrieved_artist.name == "Test Artist"

    # Clean up
    db_session.delete(artist)
    db_session.delete(user)
    db_session.commit()

# Test: Create an Artist
def test_create_artist(db_session):
    user = create_random_user(db_session)

    artist = create_artist(db_session, user)

    db_session.refresh(artist)
    assert artist.user_id == user.id

    # Clean up
    db_session.delete(artist)
    db_session.delete(user)
    db_session.commit()

# Test: Deleting User Cascades to Artist
def test_cascade_delete_user_deletes_artist(db_session):
    user = create_random_user(db_session)
    create_artist(db_session, user)

    assert get_artist_by_user_id(db_session, user.id) is not None

    db_session.delete(user)
    db_session.commit()

    artist_in_db_after = get_artist_by_user_id(db_session, user.id)
    assert artist_in_db_after is None

# Test: Get artist by username
def test_get_artist_by_username(db_session):
    user = create_random_user(db_session)
    artist = Artist(user_id=user.id, name="Username Artist", genre="Rock", bio="Rockstar")
    db_session.add(artist)
    db_session.commit()

    retrieved_artist = get_artist_by_username(db_session, user.username)
    assert retrieved_artist is not None
    assert retrieved_artist.name == "Username Artist"

    db_session.delete(artist.user)
    db_session.commit()

# Test: Get artist by username fails if not an artist
def test_get_artist_by_username_not_artist(db_session):
    user = create_random_user(db_session)
    with pytest.raises(Exception) as exc_info:
        get_artist_by_username(db_session, user.username)
    assert exc_info.value.status_code == 400
    assert "This user is not an artist." in str(exc_info.value.detail)

    # Clean up
    db_session.delete(user)
    db_session.commit()
