import pytest
from tests.utils import create_random_user, get_session
from crud.listener import get_listener_by_user_id, create_listener, get_listener_by_username

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

# Test: Get listener by user_id
def test_get_listener_by_user_id(db_session):
    user = create_random_user(db_session)
    retrieved_listener = get_listener_by_user_id(db_session, user.id)
    assert retrieved_listener is not None
    assert retrieved_listener.user_id == user.id

    # Clean up
    db_session.delete(user)
    db_session.commit()

# Test: Create a Listener
def test_create_listener(db_session):
    user = create_random_user(db_session)
    listener = get_listener_by_user_id(db_session, user.id)
    assert listener.user_id == user.id

    # Clean up
    db_session.delete(user)
    db_session.commit()

# Test: Create listener fails if user is already a listener
def test_create_listener_already_exists(db_session):
    user = create_random_user(db_session)

    with pytest.raises(Exception) as exc_info:
        create_listener(db_session, user)
    assert exc_info.value.status_code == 400
    assert "This user is already a listener." in str(exc_info.value.detail)

    # Clean up
    db_session.delete(user)
    db_session.commit()

# Test: Deleting User Cascades to Listener
def test_cascade_delete_user_deletes_listener(db_session):
    user = create_random_user(db_session)

    assert get_listener_by_user_id(db_session, user.id) is not None

    db_session.delete(user)
    db_session.commit()

    listener_in_db_after = get_listener_by_user_id(db_session, user.id)
    assert listener_in_db_after is None

# Test: Get listener by username
def test_get_listener_by_username(db_session):
    user = create_random_user(db_session)

    retrieved_listener = get_listener_by_username(db_session, user.username)
    assert retrieved_listener is not None
    assert retrieved_listener.user_id == user.id

    # Clean up
    db_session.delete(user)
    db_session.commit()
