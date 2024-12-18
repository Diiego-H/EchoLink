import pytest
from models.user import User
from metrics.listeners import get_listener_loyalty_data, loyalty_points, loyalty_sorted_listeners
from models.question import Question, ResponseEnum
from crud.listener import follow_artist, get_all_listeners
from crud.question import can_question
from tests.utils import create_artist, create_listener, get_session

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

# Test: Check if a listener can ask a question to an artist
def test_can_question(db_session):
    # Create a listener and an artist
    listener = create_listener(db_session)
    artist = create_artist(db_session)

    # Test when the listener does not follow the artist
    assert not can_question(db_session, listener, artist)

    # Make the listener follow the artist
    follow_artist(db_session, listener, artist.user.username)

    # Test when the listener follows the artist
    assert can_question(db_session, listener, artist)

    # Clean up
    db_session.delete(listener.user)
    db_session.delete(artist.user)
    db_session.commit()

# Test: Test loyalty points function
def test_loyalty_points(db_session):
    listener = create_listener(db_session)
    artist = create_artist(db_session)

    # Test with no interactions
    points = loyalty_points(artist, listener, db_session)
    assert points >= 1000  # Minimum score is 1000

    # Make the listener follow the artist
    follow_artist(db_session, listener, artist.user.username)

    # Test with following
    points = loyalty_points(artist, listener, db_session)
    assert points >= 6000  # Should add follow score

    # Add questions and responses
    question = Question(listener_id=listener.listener_id, artist_id=artist.artist_id, question_text="Sample?", response_status=ResponseEnum.answered)
    db_session.add(question)
    db_session.commit()

    # Test with answered question
    points2 = loyalty_points(artist, listener, db_session)
    assert points2 > points  # Includes follow + answered question bonus

    # Add rejected question
    question_rejected = Question(listener_id=listener.listener_id, artist_id=artist.artist_id, question_text="Sample?", response_status=ResponseEnum.rejected)
    db_session.add(question_rejected)
    db_session.commit()

    # Test with rejected question
    points3 = loyalty_points(artist, listener, db_session)
    assert points3 < points2  # Rejected reduces points

    # Clean up
    db_session.delete(listener.user)
    db_session.delete(artist.user)
    db_session.commit()

# Test: Test loyalty points sort function with listeners
def test_loyalty_sorted_listeners(db_session):
    db_session.query(User).delete()  # Deletes all rows in the User table
    db_session.commit()              # Commit the changes to the database
    
    artist = create_artist(db_session)
    listener1 = create_listener(db_session, "listener1")
    listener2 = create_listener(db_session, "listener2")

    # Make listener1 follow the artist
    follow_artist(db_session, listener1, artist.user.username)

    # Get sorted listeners
    sorted_list = loyalty_sorted_listeners(artist, db_session)
    assert sorted_list[0][0] == listener1.user.username  # Listener1 has higher score
    assert sorted_list[1][0] == listener2.user.username  # Listener2 is lower

    # Clean up
    db_session.delete(listener1.user)
    db_session.delete(listener2.user)
    db_session.delete(artist.user)
    db_session.commit()

# Test: Get listener loyalty data
def test_get_listener_loyalty_data(db_session):
    artist = create_artist(db_session)
    listener = create_listener(db_session)

    # Get listener loyalty data
    data = get_listener_loyalty_data(artist, listener, db_session)
    assert data["ranking"] == 1  # Single listener, so rank should be 1
    assert data["loyalty_points"] >= 1000  # Initial loyalty points
    assert data["percentage"] == 0  # Single listener is 0% top

    # Make listener follow the artist
    follow_artist(db_session, listener, artist.user.username)

    # Get listener loyalty data
    data = get_listener_loyalty_data(artist, listener, db_session)
    assert data["ranking"] == 1  # Single listener, so rank should be 1
    assert data["loyalty_points"] >= 6000  # Points include follow
    assert data["percentage"] == 0  # Single listener is 0% top

    # Create new listener
    listener2 = create_listener(db_session, "listener2")

    # Get listener2 loyalty data
    data2 = get_listener_loyalty_data(artist, listener2, db_session)
    assert data2["ranking"] == 2  # Two listeners, so rank should be 2
    assert data2["loyalty_points"] >= 1000  # Initial loyalty points
    assert data2["percentage"] == 50  # Listener2 is 50% top

    # Clean up
    db_session.delete(listener2.user)
    db_session.delete(listener.user)
    db_session.delete(artist.user)
    db_session.commit()

# Test: Get all listeners
def test_get_all_listeners(db_session):
    # Retrieve all listeners
    n_listeners = len(get_all_listeners(db_session))

    # Create two listeners
    listener1 = create_listener(db_session)
    listener2 = create_listener(db_session, "listener2")
    
    # Retrieve all listeners
    all_listeners = get_all_listeners(db_session)

    # Ensure the listeners created are in the result
    assert len(all_listeners) == n_listeners + 2
    ids = [listener.listener_id for listener in all_listeners]
    assert listener1.listener_id in ids
    assert listener2.listener_id in ids

    # Cleanup created users
    db_session.delete(listener1.user)
    db_session.delete(listener2.user)
    db_session.commit()
