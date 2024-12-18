import pytest
from models.user import RoleEnum, UserInput, VisibilityEnum
from crud.user import create_user
from tests.utils import get_session

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

def test_create_user_with_image_url(db_session):
    # Define user input including a valid image URL
    user_input = UserInput(
        username="testuser",
        email="testuser@example.com",
        password="securepassword",
        description="Test user description",
        genre="Rock",
        visibility=VisibilityEnum.public,
        role=RoleEnum.artist,
        image_url="https://example.com/image.jpg"  # Valid image URL
    )

    # Call create_user function
    user = create_user(db_session, user_input)

    # Assertions
    assert user.username == "testuser"
    assert user.email == "testuser@example.com"
    assert user.image_url == "https://example.com/image.jpg"

    # Delete data created
    db_session.delete(user)
    db_session.commit()


def test_create_user_without_image_url(db_session):
    # Define user input without an image URL
    user_input = UserInput(
        username="testuser",
        email="testuser@example.com",
        password="securepassword",
        description="Test user description",
        genre="Rock",
        visibility=VisibilityEnum.public,
        role=RoleEnum.artist
    )

    # Call create_user function
    user = create_user(db_session, user_input)

    # Assertions
    assert user.username == "testuser"
    assert user.email == "testuser@example.com"
    assert user.image_url is None  # Default behavior when no image URL is provided

    # Delete data created
    db_session.delete(user)
    db_session.commit()




