import pytest
from datetime import datetime
from fastapi import HTTPException
from crud.listener import follow_artist
from models.question import Question, QuestionInput, QuestionResponse, ResponseEnum
from crud.question import get_questions_by_listener, get_questions_by_artist, submit_question, get_question_by_id, response_question
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

# Test: Get questions by listener username
def test_get_questions_by_listener(db_session):
    listener = create_listener(db_session)
    artist = create_artist(db_session)

    question = Question(listener_id=listener.listener_id, artist_id=artist.artist_id, question_text="What is your favorite song?", question_date=datetime.utcnow())
    db_session.add(question)
    db_session.commit()

    retrieved_questions = get_questions_by_listener(db_session, listener.user.username)
    assert len(retrieved_questions) > 0
    assert retrieved_questions[0].listener_id == listener.listener_id

    # Delete data created
    db_session.delete(listener.user)
    db_session.delete(artist.user)
    db_session.commit()

# Test: Get questions by artist username
def test_get_questions_by_artist(db_session):
    listener = create_listener(db_session)
    artist = create_artist(db_session)

    question = Question(listener_id=listener.listener_id, artist_id=artist.artist_id, question_text="What is your favorite song?", question_date=datetime.utcnow())
    db_session.add(question)
    db_session.commit()

    retrieved_questions = get_questions_by_artist(db_session, artist.user.username)
    assert len(retrieved_questions) > 0
    assert retrieved_questions[0].artist_id == artist.artist_id

    # Delete data created
    db_session.delete(listener.user)
    db_session.delete(artist.user)
    db_session.commit()

# Test: Submit a question
def test_submit_question(db_session):
    listener = create_listener(db_session)
    artist = create_artist(db_session)

    # Make the listener follows the artist
    follow_artist(db_session, listener, artist.user.username)

    question_input = QuestionInput(
        artist_username=artist.user.username,
        question_text="What is your favorite song?"
    )

    question = submit_question(db_session, listener, question_input)
    db_session.refresh(question)

    assert question.listener_id == listener.listener_id
    assert question.artist_id == artist.artist_id
    assert question.question_text == "What is your favorite song?"
    assert question.response_status == ResponseEnum.waiting

    # Delete data created
    db_session.delete(listener.user)
    db_session.delete(artist.user)
    db_session.commit()

# Test: Get question by id
def test_get_question_by_id(db_session):
    listener = create_listener(db_session)
    artist = create_artist(db_session)

    question = Question(listener_id=listener.listener_id, artist_id=artist.artist_id, question_text="What is your favorite song?", question_date=datetime.utcnow())
    db_session.add(question)
    db_session.commit()

    retrieved_question = get_question_by_id(db_session, question.question_id)
    assert retrieved_question is not None
    assert retrieved_question.question_id == question.question_id

    # Delete data created
    db_session.delete(listener.user)
    db_session.delete(artist.user)
    db_session.commit()

# Test: Response to a question
def test_response_question(db_session):
    listener = create_listener(db_session)
    artist = create_artist(db_session)

    question = Question(listener_id=listener.listener_id, artist_id=artist.artist_id, question_text="What is your favorite song?", question_date=datetime.utcnow())
    db_session.add(question)
    db_session.commit()

    response = QuestionResponse(question_id=question.question_id, response_text="I love this song!")
    answered_question = response_question(db_session, artist, response, ResponseEnum.answered)

    assert answered_question.response_status == ResponseEnum.answered
    assert answered_question.response_text == "I love this song!"

    # Delete data created
    db_session.delete(listener.user)
    db_session.delete(artist.user)
    db_session.commit()

# Test: Artist not answering others question
def test_artist_cannot_answer_others_question(db_session):
    # Create listeners and two artists
    listener = create_listener(db_session)
    artist_1 = create_artist(db_session)
    artist_2 = create_artist(db_session, "artist2")

    # Make the listener follows the artist_1
    follow_artist(db_session, listener, artist_1.user.username)

    # Listener asks a question to artist_1
    question_input = QuestionInput(
        listener_username=listener.user.username,
        artist_username=artist_1.user.username,
        question_text="What is your favorite genre of music?"
    )
    question = submit_question(db_session, listener, question_input)

    # Artist_2 tries to answer the question meant for artist_1
    response = QuestionResponse(question_id=question.question_id, response_text="I love rock music!")
    
    with pytest.raises(HTTPException) as excinfo:
        response_question(db_session, artist_2, response, ResponseEnum.answered)

    # Assert the exception is due to forbidden access
    assert excinfo.value.status_code == 403
    assert excinfo.value.detail == "This artist cannot answer this question."

    # Delete data created
    db_session.delete(listener.user)
    db_session.delete(artist_1.user)
    db_session.delete(artist_2.user)
    db_session.commit()