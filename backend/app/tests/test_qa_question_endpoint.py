from tests.utils import get_session, get_client, create_random_auth_artist, create_random_auth_user, random_lower_string
from models.question import Question
from models.user import User
from crud.listener import follow_artist, get_listener_by_username

def test_create_question_successful():
    db = get_session()
    client = get_client()

    # Create an authenticated listener
    listener = create_random_auth_user(db)
    artist = create_random_auth_artist(db)

    # Make the listener follows the artist
    follow_artist(db, get_listener_by_username(db, listener.username), artist.username)

    # Question data
    question_data = {
        "question_text": random_lower_string(),
        "artist_username": artist.username
    }

    headers = {"Authorization": f"Bearer {listener.token}"}
    response = client.post("/questions/", json=question_data, headers=headers)

    assert response.status_code == 200
    question = response.json()
    assert question["question_text"] == question_data["question_text"]
    assert question["response_status"] == "waiting"

    # Check if the question is created
    db_question = db.query(Question).filter(Question.question_text == question_data["question_text"]).first()
    assert db_question is not None

    # Clean up
    db.delete(db_question)
    db.delete(artist)
    db.delete(listener)
    db.commit()

    # Check if the question is deleted
    db_question = db.query(Question).filter(Question.question_text == question_data["question_text"]).first()
    assert db_question is None

    # Check if the user is deleted
    db_listener = db.query(User).filter(User.id == listener.id).first()
    assert db_listener is None

    db_artist = db.query(User).filter(User.id == artist.id).first()
    assert db_artist is None

def test_two_questions_error():
    db = get_session()
    client = get_client()

    # Create an authenticated listener
    listener = create_random_auth_user(db)
    artist = create_random_auth_artist(db)
    
    # Make the listener follows the artist
    follow_artist(db, get_listener_by_username(db, listener.username), artist.username)

    # Question data
    question_data = {
        "question_text": random_lower_string(),
        "artist_username": artist.username
    }

    headers = {"Authorization": f"Bearer {listener.token}"}
    response = client.post("/questions/", json=question_data, headers=headers)

    assert response.status_code == 200

    response = client.post("/questions/", json=question_data, headers=headers)
    assert response.status_code == 403
    assert response.json() == {"detail": "This listener cannot ask this artist."}

    # Check if the question is created
    db_question = db.query(Question).filter(Question.question_text == question_data["question_text"]).first()
    assert db_question is not None

    # Clean up
    db.delete(db_question)
    db.delete(artist)
    db.delete(listener)
    db.commit()

    # Check if the question is deleted
    db_question = db.query(Question).filter(Question.question_text == question_data["question_text"]).first()
    assert db_question is None

    # Check if the user is deleted
    db_listener = db.query(User).filter(User.id == listener.id).first()
    assert db_listener is None

    db_artist = db.query(User).filter(User.id == artist.id).first()
    assert db_artist is None

def test_response_question_successful():
    db = get_session()
    client = get_client()

    # Create an authenticated listener
    listener = create_random_auth_user(db)
    artist = create_random_auth_artist(db)
    
    # Make the listener follows the artist
    follow_artist(db, get_listener_by_username(db, listener.username), artist.username)

    # Question data
    question_data = {
        "question_text": random_lower_string(),
        "artist_username": artist.username
    }

    headersL = {"Authorization": f"Bearer {listener.token}"}
    response = client.post("/questions/", json=question_data, headers=headersL)

    assert response.status_code == 200

    question_response = {
        "question_id": response.json()["question_id"],
        "response_text": random_lower_string()
    }

    headersA = {"Authorization": f"Bearer {artist.token}"}
    response = client.post("/questions/answer", json=question_response, headers=headersA)

    assert response.status_code == 200

    # Check if the question is created
    db_question = db.query(Question).filter(Question.question_text == question_data["question_text"]).first()
    assert db_question is not None

    # Clean up
    db.delete(db_question)
    db.delete(artist)
    db.delete(listener)
    db.commit()

    # Check if the question is deleted
    db_question = db.query(Question).filter(Question.question_text == question_data["question_text"]).first()
    assert db_question is None

    # Check if the user is deleted
    db_listener = db.query(User).filter(User.id == listener.id).first()
    assert db_listener is None

    db_artist = db.query(User).filter(User.id == artist.id).first()
    assert db_artist is None

def test_answer_question_not_found():
    db = get_session()
    client = get_client()

    # Create an authenticated listener
    listener = create_random_auth_user(db)
    artist = create_random_auth_artist(db)
    
    # Make the listener follows the artist
    follow_artist(db, get_listener_by_username(db, listener.username), artist.username)

    # Question data
    question_data = {
        "question_text": random_lower_string(),
        "artist_username": artist.username
    }

    headersL = {"Authorization": f"Bearer {listener.token}"}
    response = client.post("/questions/", json=question_data, headers=headersL)

    assert response.status_code == 200

    question_response = {
        "question_id": 5555,
        "response_text": random_lower_string()
    }

    headersA = {"Authorization": f"Bearer {artist.token}"}
    response = client.post("/questions/answer", json=question_response, headers=headersA)

    assert response.status_code == 404
    assert response.json() == {"detail": "Question not found."}

    # Check if the question is created
    db_question = db.query(Question).filter(Question.question_text == question_data["question_text"]).first()
    assert db_question is not None

    # Clean up
    db.delete(db_question)
    db.delete(artist)
    db.delete(listener)
    db.commit()

    # Check if the question is deleted
    db_question = db.query(Question).filter(Question.question_text == question_data["question_text"]).first()
    assert db_question is None

    # Check if the user is deleted
    db_listener = db.query(User).filter(User.id == listener.id).first()
    assert db_listener is None

    db_artist = db.query(User).filter(User.id == artist.id).first()
    assert db_artist is None

def test_response_artist_no_permissions():
    db = get_session()
    client = get_client()

    # Create an authenticated listener
    listener = create_random_auth_user(db)
    artist = create_random_auth_artist(db)
    artist2 = create_random_auth_artist(db)

    # Make the listener follows the artist
    follow_artist(db, get_listener_by_username(db, listener.username), artist.username)

    # Question data
    question_data = {
        "question_text": random_lower_string(),
        "artist_username": artist.username
    }

    headersL = {"Authorization": f"Bearer {listener.token}"}
    response = client.post("/questions/", json=question_data, headers=headersL)

    assert response.status_code == 200

    question_response = {
        "question_id": response.json()["question_id"],
        "response_text": random_lower_string()
    }

    headersA2 = {"Authorization": f"Bearer {artist2.token}"}
    response = client.post("/questions/answer", json=question_response, headers=headersA2)

    assert response.status_code == 403
    assert response.json() == {"detail": "This artist cannot answer this question."}

    # Check if the question is created
    db_question = db.query(Question).filter(Question.question_text == question_data["question_text"]).first()
    assert db_question is not None

    # Clean up
    db.delete(db_question)
    db.delete(artist)
    db.delete(artist2)
    db.delete(listener)
    db.commit()

    # Check if the question is deleted
    db_question = db.query(Question).filter(Question.question_text == question_data["question_text"]).first()
    assert db_question is None

    # Check if the user is deleted
    db_listener = db.query(User).filter(User.id == listener.id).first()
    assert db_listener is None

    db_artist = db.query(User).filter(User.id == artist.id).first()
    assert db_artist is None
    
def test_reject_question_successful():
    db = get_session()
    client = get_client()

    # Create an authenticated listener
    listener = create_random_auth_user(db)
    artist = create_random_auth_artist(db)
    
    # Make the listener follows the artist
    follow_artist(db, get_listener_by_username(db, listener.username), artist.username)

    # Question data
    question_data = {
        "question_text": random_lower_string(),
        "artist_username": artist.username
    }

    headersL = {"Authorization": f"Bearer {listener.token}"}
    response = client.post("/questions/", json=question_data, headers=headersL)

    assert response.status_code == 200

    question_response = {
        "question_id": response.json()["question_id"],
        "response_text": random_lower_string()
    }

    headersA = {"Authorization": f"Bearer {artist.token}"}
    response = client.post("/questions/reject", json=question_response, headers=headersA)

    assert response.status_code == 200

    # Check if the question is created
    db_question = db.query(Question).filter(Question.question_text == question_data["question_text"]).first()
    assert db_question is not None

    # Clean up
    db.delete(db_question)
    db.delete(artist)
    db.delete(listener)
    db.commit()

    # Check if the question is deleted
    db_question = db.query(Question).filter(Question.question_text == question_data["question_text"]).first()
    assert db_question is None

    # Check if the user is deleted
    db_listener = db.query(User).filter(User.id == listener.id).first()
    assert db_listener is None

    db_artist = db.query(User).filter(User.id == artist.id).first()
    assert db_artist is None
