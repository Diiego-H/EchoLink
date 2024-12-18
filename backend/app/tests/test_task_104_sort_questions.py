import pytest
from datetime import datetime
from crud.listener import follow_artist, get_listener_by_listener_id
from models.question import Question, ResponseEnum
from crud.question import get_questions_by_listener, get_waiting_questions_by_artist
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


# Test: Get listener by listener_id
def test_get_listener_by_listener_id(db_session):
    listener = create_listener(db_session)
    id = listener.listener_id

    # Fetch the listener by their listener_id
    retrieved_listener = get_listener_by_listener_id(db_session, id)

    # Assertions
    assert retrieved_listener is not None
    assert retrieved_listener.listener_id == listener.listener_id
    assert retrieved_listener.user_id == listener.user_id

    # Cleanup
    db_session.delete(listener.user)
    db_session.commit()

    # Fetch a None listener
    assert get_listener_by_listener_id(db_session, id) is None


# Test: Get questions by listener username
def test_get_questions_by_listener(db_session):
    # Setup: Create listener, artist, and questions
    listener = create_listener(db_session)
    artist = create_artist(db_session)
    questions = [
        Question(listener_id=listener.listener_id, artist_id=artist.artist_id, question_text="Answered question",
                 response_status=ResponseEnum.answered, response_date=datetime(2023, 10, 2), archived=False,
                 question_date=datetime(2023, 10, 1)),
        Question(listener_id=listener.listener_id, artist_id=artist.artist_id, question_text="Answered2 question",
                 response_status=ResponseEnum.answered, response_date=datetime(2023, 10, 3), archived=False,
                 question_date=datetime(2023, 10, 1)),
        Question(listener_id=listener.listener_id, artist_id=artist.artist_id, question_text="Rejected question",
                 response_status=ResponseEnum.rejected, response_date=datetime(2023, 10, 3), archived=False,
                 question_date=datetime(2023, 10, 1)),
        Question(listener_id=listener.listener_id, artist_id=artist.artist_id, question_text="Waiting question",
                 response_status=ResponseEnum.waiting, response_date=None, archived=False,
                 question_date=datetime(2023, 10, 4)),
        Question(listener_id=listener.listener_id, artist_id=artist.artist_id, question_text="Answered archived",
                 response_status=ResponseEnum.answered, response_date=datetime(2023, 10, 2), archived=True,
                 question_date=datetime(2023, 10, 1)),
        Question(listener_id=listener.listener_id, artist_id=artist.artist_id, question_text="Rejected archived",
                 response_status=ResponseEnum.rejected, response_date=datetime(2023, 10, 2), archived=True,
                 question_date=datetime(2023, 10, 1)),
        Question(listener_id=listener.listener_id, artist_id=artist.artist_id, question_text="Archived waiting question",
                 response_status=ResponseEnum.waiting, response_date=None, archived=True,
                 question_date=datetime(2023, 10, 5)),
        Question(listener_id=listener.listener_id, artist_id=artist.artist_id, question_text="Archived2 waiting question",
                 response_status=ResponseEnum.waiting, response_date=None, archived=True,
                 question_date=datetime(2023, 10, 6)),
    ]
    db_session.add_all(questions)
    db_session.commit()

    # Call the function
    sorted_questions = get_questions_by_listener(db_session, listener.user.username)

    # Assertions
    assert sorted_questions[0].response_status == ResponseEnum.answered  # Answered comes first
    assert sorted_questions[0].question_text == "Answered2 question"     # In case of a draw, first the recent ones by response_date
    assert sorted_questions[0].archived is False                         # Non-archived first
    assert sorted_questions[1].response_status == ResponseEnum.answered
    assert sorted_questions[1].question_text == "Answered question"    
    assert sorted_questions[1].archived is False  

    assert sorted_questions[2].response_status == ResponseEnum.rejected  # Rejected second
    assert sorted_questions[2].archived is False

    assert sorted_questions[3].response_status == ResponseEnum.waiting   # Waiting third
    assert sorted_questions[3].archived is False

    assert sorted_questions[4].response_status == ResponseEnum.answered  # Archived comes last
    assert sorted_questions[4].archived is True

    assert sorted_questions[5].response_status == ResponseEnum.rejected
    assert sorted_questions[5].archived is True

    assert sorted_questions[6].response_status == ResponseEnum.waiting   # In case of a draw, first the recent ones by question_date
    assert sorted_questions[6].archived is True
    assert sorted_questions[6].question_text == "Archived2 waiting question"

    assert sorted_questions[7].response_status == ResponseEnum.waiting
    assert sorted_questions[7].archived is True
    assert sorted_questions[7].question_text == "Archived waiting question"

    # Clean up
    db_session.delete(listener.user)
    db_session.delete(artist.user)
    db_session.commit()


# Test: Get questions by artist username
def test_get_questions_by_artist(db_session):
    # Setup: Create artist, listeners, and questions
    artist = create_artist(db_session)
    listener1 = create_listener(db_session, "listener1")
    listener2 = create_listener(db_session, "listener2")

    # No questions yet
    assert len(get_waiting_questions_by_artist(db_session, artist.user.username)) == 0

    questions = [
        Question(listener_id=listener1.listener_id, artist_id=artist.artist_id, question_text="Answered question",
                 response_status=ResponseEnum.answered, response_date=datetime(2023, 10, 2), archived=False,
                 question_date=datetime(2023, 10, 1)),
        Question(listener_id=listener1.listener_id, artist_id=artist.artist_id, question_text="Rejected question",
                 response_status=ResponseEnum.rejected, response_date=datetime(2023, 10, 3), archived=False,
                 question_date=datetime(2023, 10, 1)),
        Question(listener_id=listener1.listener_id, artist_id=artist.artist_id, question_text="Waiting recent question",
                 response_status=ResponseEnum.waiting, response_date=None, archived=True,
                 question_date=datetime(2023, 10, 5)),
        Question(listener_id=listener1.listener_id, artist_id=artist.artist_id, question_text="Waiting old question",
                 response_status=ResponseEnum.waiting, response_date=None, archived=False,
                 question_date=datetime(2023, 10, 4)),

        Question(listener_id=listener2.listener_id, artist_id=artist.artist_id, question_text="Waiting question",
                 response_status=ResponseEnum.waiting, response_date=datetime(2023, 10, 2), archived=True,
                 question_date=datetime(2023, 10, 1))
    ]
    db_session.add_all(questions)
    db_session.commit()

    # Listener1 follows the artist
    follow_artist(db_session, listener1, artist.user.username)

    # Call the function
    sorted_questions = get_waiting_questions_by_artist(db_session, artist.user.username)

    # Assertions
    assert len(sorted_questions) == 3  # Only waiting questions should be retrieved
    assert all([question.response_status == ResponseEnum.waiting for question in sorted_questions])

    assert sorted_questions[0].listener_id == listener1.listener_id  # Listener1 should come first (higher loyalty)
    assert sorted_questions[1].listener_id == listener1.listener_id
    assert sorted_questions[2].listener_id == listener2.listener_id  # Listener2 should come second

    assert sorted_questions[0].question_text == "Waiting old question"  # Old question should come first

    # Clean up
    db_session.delete(listener1.user)
    db_session.delete(listener2.user)
    db_session.delete(artist.user)
    db_session.commit()
