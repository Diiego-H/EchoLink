import pytest
from tests.utils import create_random_artist, create_random_auth_listener, get_session
from crud.listener import get_sorted_artists, follow_artist, get_listener_by_user_id

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

def test_sort_artists(db_session):
    
    user = create_random_auth_listener(db_session)
    listener = get_listener_by_user_id(db_session, user.id)

    artist1 = create_random_artist(db_session)
    artist2 = create_random_artist(db_session)
    artist3 = create_random_artist(db_session)
    artist4 = create_random_artist(db_session)

    # Follow artists
    follow_artist(db_session, listener, artist4.user.username)

    # Sort artists
    artists = get_sorted_artists(db_session, user.id)

    assert len(artists) == 4
    assert artists[0].user.username == artist4.user.username
    assert artists[1].user.username == artist1.user.username
    assert artists[2].user.username == artist2.user.username
    assert artists[3].user.username == artist3.user.username

    # Clean up artists
    db_session.delete(artist1.user)
    db_session.delete(artist2.user)
    db_session.delete(artist3.user)
    db_session.delete(artist4.user)

    # Clean up user
    db_session.delete(user)

    # Commit the transaction
    db_session.commit()

