from sqlalchemy.orm import Session
from datetime import datetime
from models.question import Question, QuestionInput, QuestionResponse, ResponseEnum
from fastapi import HTTPException, status
from crud.artist import get_artist_by_username
from crud.listener import check_follow, get_listener_by_username, get_listener_by_listener_id
from models.listener import Listener
from models.artist import Artist
from metrics.listeners import get_listener_loyalty_data, loyalty_points

# Get questions by listener username
def get_questions_by_listener(db: Session, username: str):
    listener = get_listener_by_username(db, username)
    questions = db.query(Question).filter(Question.listener_id == listener.listener_id).all()

    # Define sorting function
    def sort_key(question):
        # First sort by response_status (answered > rejected > waiting)
        status_priority = {
            ResponseEnum.answered: 0,
            ResponseEnum.rejected: 1,
            ResponseEnum.waiting: 2
        }

        # Determine priority based on response status
        status_sort_value = status_priority.get(question.response_status, 3)
        assert status_sort_value != 3, f"Invalid response status: {question.response_status}"

        # If the question is 'waiting', use question_date for the tie-breaking
        # If not 'waiting', use response_date
        date_value = question.question_date if question.response_status == ResponseEnum.waiting else question.response_date

        # Use negative timestamp to sort in descending order (recent questions first)
        date_sort_value = -date_value.timestamp()

        # Determine if the question is archived or not
        archived_sort_value = 1 if question.archived else 0  # Non-archived first (0 before 1)

        # Return a tuple with sorting priorities
        return (archived_sort_value, status_sort_value, date_sort_value)

    # Sort questions using the custom sort key
    sorted_questions = sorted(questions, key=sort_key)

    return sorted_questions

# Get questions by artist username
def get_questions_by_artist(db: Session, username: str):
    artist = get_artist_by_username(db, username)
    return db.query(Question).filter(Question.artist_id == artist.artist_id).all()

# Get waiting questions by artist username
def get_waiting_questions_by_artist(db: Session, username: str):
    artist = get_artist_by_username(db, username)
    questions = db.query(Question).filter(Question.artist_id == artist.artist_id,
                                          Question.response_status == ResponseEnum.waiting).all()

    # Sort by score first (descending), then by date (ascending) in case of a draw
    return sorted(questions, key=lambda x: 
                  (-loyalty_points(artist, get_listener_by_listener_id(db, x.listener_id), db),
                   x.question_date))

# Decide if a listener can ask a question to an artist
def can_question(db: Session, listener: Listener, artist: Artist):
    # Check if listener follows the artist
    if not check_follow(db, listener, artist.user.username):
        return False
    
    if db.query(Question).filter(Question.listener_id == listener.listener_id, 
                                Question.artist_id == artist.artist_id,
                                Question.response_status == ResponseEnum.waiting).first():
        return False
    
    # Check if listener is in the top 10 in terms of loyalty
    return True
    return get_listener_loyalty_data(artist, listener, db)["percentage"] < 10

# Add a new question to the database
def submit_question(db: Session, listener: Listener, question_input: QuestionInput) -> Question:
    artist = get_artist_by_username(db, question_input.artist_username)

    # Decide if the listener can ask a question to the artist
    if not can_question(db, listener, artist):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This listener cannot ask this artist.")
    
    # Check if a question the listener is waiting for a response from the artist
    if db.query(Question).filter(Question.listener_id == listener.listener_id, 
                                 Question.artist_id == artist.artist_id,
                                 Question.response_status == ResponseEnum.waiting).first():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="This listener is waiting for a response.")

    # Create Question
    question = Question(
        listener_id=listener.listener_id,
        artist_id=artist.artist_id,
        artist_username=artist.user.username,
        listener_username=listener.user.username,
        question_text=question_input.question_text,
        response_status = ResponseEnum.waiting,
        question_date=datetime.utcnow()
    )

    # Add question to the session and commit it
    db.add(question)
    db.commit()
    db.refresh(question)

    return question

# Get a question by its id
def get_question_by_id(db: Session, question_id: int):
    return db.query(Question).filter(Question.question_id == question_id).first()

# Response a question from an artist
def response_question(db: Session, artist: Artist, response: QuestionResponse, response_status: ResponseEnum) -> Question:
    question = get_question_by_id(db, response.question_id)
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found.")
    
    if question.artist_id != artist.artist_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This artist cannot answer this question.")
    
    if question.response_status != ResponseEnum.waiting:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="This question has already been responded.")
    
    # Update question
    question.response_text = response.response_text
    question.response_date = datetime.utcnow()
    question.response_status = response_status
    db.commit()
    db.refresh(question)
    return question
    
# Archive a question
def archive_question(db: Session, question_id: int, listener: Listener) -> Question:
    question = get_question_by_id(db, question_id)
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found.")
    
    if question.listener_id != listener.listener_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This listener cannot archive this question.")
    
    question.archived = True
    db.commit()
    db.refresh(question)
    return question