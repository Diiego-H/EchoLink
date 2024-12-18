import pytest
from models.user import RoleEnum
from crud.user import get_role, create_user
from crud.listener import get_listener_by_user_id
from crud.artist import get_artist_by_user_id
from tests.utils import create_random_user, get_session, create_random_user_input

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

### Tests for assign_role ###

def test_create_user_assigns_listener(db_session):
    # Act
    user = create_random_user(db_session)

    # Assert
    assert user.role == RoleEnum.listener

    # Listener created
    assert get_listener_by_user_id(db_session, user.id) is not None

    # Clean up
    db_session.delete(user)
    db_session.commit()

def test_create_user_assigns_artist(db_session):
    # Arrange
    user_input = create_random_user_input()
    user_input.role = RoleEnum.artist
    user = create_user(db_session, user_input)

    # Assert
    assert user.role == RoleEnum.artist

    # Artist created
    assert get_artist_by_user_id(db_session, user.id) is not None

    # Delete data created
    db_session.delete(user)
    db_session.commit()

### Tests for get_role ###

def test_get_role_of_user_with_role(db_session):
    # Arrange
    user = create_random_user(db_session)

    # Act
    role = get_role(user)

    # Assert
    assert role == RoleEnum.listener

    # Clean up
    db_session.delete(user)
    db_session.commit()
