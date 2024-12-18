import pytest
from datetime import datetime
from fastapi import HTTPException
from models.question import Question
from crud.question import archive_question, get_question_by_id
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


# Test: Get question by ID and verify archived field (default is False)
def test_get_question_by_id_archived_default(db_session):
    listener = create_listener(db_session)
    artist = create_artist(db_session)

    # Create a question
    question = Question(listener_id=listener.listener_id, artist_id=artist.artist_id, question_text="What is your favorite song?", question_date=datetime.utcnow())
    db_session.add(question)
    db_session.commit()

    # Retrieve question by ID
    retrieved_question = get_question_by_id(db_session, question.question_id)
    assert retrieved_question is not None
    assert retrieved_question.archived is False

    # Delete data created
    db_session.delete(listener.user)
    db_session.delete(artist.user)
    db_session.commit()
    

# Test: Archive a question
def test_archive_question(db_session):
    listener = create_listener(db_session)
    artist = create_artist(db_session)

    # Listener submits a question
    question = Question(listener_id=listener.listener_id, artist_id=artist.artist_id, question_text="What is your favorite song?", question_date=datetime.utcnow())
    db_session.add(question)
    db_session.commit()

    # Archive the question
    archived_question = archive_question(db_session, question.question_id, listener)
    assert archived_question.archived is True

    # Verify that the archived field is updated in the database
    db_session.refresh(archived_question)
    assert archived_question.archived is True

    # Test forbidden case (another listener tries to archive)
    listener2 = create_listener(db_session, name="listener2")
    with pytest.raises(HTTPException) as excinfo:
        archive_question(db_session, question.question_id, listener2)
    assert excinfo.value.status_code == 403
    assert excinfo.value.detail == "This listener cannot archive this question."

    # Delete data created
    db_session.delete(listener2.user)
    db_session.delete(listener.user)
    db_session.delete(artist.user)
    db_session.commit()


# Test: Get question by ID after archiving
def test_get_question_by_id_after_archiving(db_session):
    listener = create_listener(db_session)
    artist = create_artist(db_session)

    # Create a question
    question = Question(listener_id=listener.listener_id, artist_id=artist.artist_id, question_text="What is your favorite song?", question_date=datetime.utcnow())
    db_session.add(question)
    db_session.commit()

    # Retrieve question by ID
    retrieved_question = get_question_by_id(db_session, question.question_id)
    assert retrieved_question is not None
    assert retrieved_question.archived is False

    # Archive the question
    question.archived = True
    db_session.commit()

    # Retrieve question by ID
    retrieved_question = get_question_by_id(db_session, question.question_id)
    assert retrieved_question is not None
    assert retrieved_question.archived is True

    # Delete data created
    db_session.delete(listener.user)
    db_session.delete(artist.user)
    db_session.commit()