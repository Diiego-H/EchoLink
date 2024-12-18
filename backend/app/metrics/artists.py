
from crud.artist import get_followers, get_all_artists, get_artist_by_username
from crud.question import get_questions_by_artist, can_question
from crud.listener import get_listener_by_user_id, check_follow
from models.artist import ArtistOutput
from models.question import ResponseEnum
from pytest import Session
from fastapi import HTTPException


def reply_rate_score(artist_name: str, db: Session) -> float:
    # Fetch all questions for the artist
    all_questions = get_questions_by_artist(db, artist_name)

    # Total counts for each status
    answered = sum(1 for question in all_questions if question.response_status == ResponseEnum.answered)
    rejected = sum(1 for question in all_questions if question.response_status == ResponseEnum.rejected)
    waiting = sum(1 for question in all_questions if question.response_status == ResponseEnum.waiting)

    
    # Avoid division by zero
    if answered + rejected == 0:
        return 0.0  # No answered or rejected questions, rate is 0%

    # Calculate the answer rate
    answer_rate = (answered / (answered + rejected + waiting//2)) * 100

    # Return the rate rounded to 2 decimal places
    return round(answer_rate, 2)


def engage_artist_score(artist_name: str, db: Session) -> int:
    # Get the reply rate
    reply_rate = reply_rate_score(artist_name, db)  # Returns a percentage (0-100)

    # Get the number of followers
    followers = get_followers(db, artist_name)  # Returns an integer

    # Get all questions for the artist
    all_questions = get_questions_by_artist(db, artist_name)
    total_questions = len(all_questions) 

    # Calculate the weighted engagement score
    engage_score = 1000 + (reply_rate * 50) + (followers * 1.5) + (total_questions * 5)

    # Return the score as an integer
    return int(round(engage_score))


def get_my_ranking(artist_name: str, db: Session):
    # Check if the artist exists
    get_artist_by_username(db, artist_name)

    # Get the engagement scores for all artists
    all_artists = get_all_artists(db)
    all_scores = {artist.username: engage_artist_score(artist.username, db) for artist in all_artists}

    # Sort the scores in descending order
    sorted_scores = sorted(all_scores.items(), key=lambda x: x[1], reverse=True)

    # Initialize variables for ranking
    rank = 1
    previous_score = None
    artist_rank = None

    # Iterate through the sorted scores to assign ranks
    for i, (name, score) in enumerate(sorted_scores, start=1):
        # If the score is different from the previous score, update the rank
        if score != previous_score:
            rank = i
        # If the current artist matches the input artist, store their rank
        if name == artist_name:
            artist_rank = rank
        # Update the previous score
        previous_score = score

    if artist_rank is None:
        raise HTTPException(status_code=404, detail="Artist not found.")
    # Return the rank of the artist
    return artist_rank


def rank_data(artist_name: str, db: Session) -> dict:
    """
    Computes the ranking tier and percentage position of an artist.
    
    Args:
        artist_name (str): The name of the artist.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the tier and percentage position within the tier.
    """
    # Get the rank of the artist
    artist_rank = get_my_ranking(artist_name, db)

    # Get the number of artists
    N = len(get_all_artists(db))

    # Define the tiers
    tiers = {
        0: (1, 9),
        1: (10, 50),
        2: (51, 99),
        3: (100, 999),
        4: (1000, N if N >= 1000 else float("inf"))  # Tier 4 includes all artists beyond rank 1000
    }

    # Determine the tier and its range
    for tier, (start, end) in tiers.items():
        if start <= artist_rank <= end:
            # Calculate percentage position within the tier
            range_size = end - start + 1
            percentage = ((artist_rank - start) / range_size) * 100
            return {
                "ranking": artist_rank,
                "tier": tier,
                "percentage": int(percentage)
            }

    # This should not be reached if tiers are correctly defined
    raise HTTPException(status_code=404, detail="Could not determine the tier for the artist.")

# Get all artists with their rank_data
def get_all_artists_with_rank_data(db: Session, user_id : str = None):
    artists = get_all_artists(db)

    listener = get_listener_by_user_id(db, user_id) if user_id else None
    print(listener)
    return [
        ArtistOutput(
            username=artist.username,
            email=artist.email,
            genre=artist.genre,
            description=artist.description,
            visibility=artist.visibility,
            role=artist.role,
            image_url=artist.image_url,
            rank_data=rank_data(artist.username, db),
            can_ask=can_question(db, listener, get_artist_by_username(db, artist.username))if listener else False,
            is_following=check_follow(db, listener, artist.username) if listener else False
        )
        for artist in artists
    ]