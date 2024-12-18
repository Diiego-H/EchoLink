from fastapi import APIRouter, Depends
from crud.listener import get_listener_by_username
from metrics.artists import reply_rate_score, engage_artist_score, rank_data
from metrics.listeners import loyalty_points
from crud.artist import get_followers, get_artist_by_username
from pytest import Session
from core.config import get_db
from core.security import CurrentUser

router = APIRouter()

@router.get("/response_rate", response_model=float)
def get_artist_reply_rate(artist_name: str, db: Session = Depends(get_db)) -> float:
    """
    Calculate and return the reply rate of an artist.

    The reply rate is a metric that measures how frequently the artist responds to questions or interactions.

    Args:
        artist (Artist): The artist object containing data about their interactions and responses.

    Returns:
        float: The reply rate of the artist as a floating-point number.
    """
    return reply_rate_score(artist_name, db)


@router.get("/engagement_rate", response_model=float)
def get_artist_engagement_rate(artist_name: str, db: Session = Depends(get_db)) -> float:
    """
    Calculate and return the engagement rate of an artist.

    The engagement rate evaluates how actively the artist interacts with their audience, factoring in their responses and follower base.

    Args:
        artist (Artist): The artist object containing data about their interactions, responses, and followers.

    Returns:
        float: The engagement rate of the artist as a floating-point number.
    """
    return engage_artist_score(artist_name, db)


@router.get("/followers", response_model=int)
def get_artist_followers(artist_name: str, db: Session = Depends(get_db)) -> int:
    """
    Retrieve and return the total number of followers for an artist.

    The number of followers is a key metric that reflects the size of the artist's audience.

    Args:
        artist (Artist): The artist object containing data about their profile and audience.

    Returns:
        int: The total number of followers the artist has as an integer.
    """
    return get_followers(db, artist_name)



@router.get("/ranking", response_model=dict)
def get_artist_rank_data(artist_name: str, db: Session = Depends(get_db)) -> dict:
    """
    Retrieve and return the rank_data for an artist.

    Args:
        artist_name (str): The artist name.

    Returns:
        dict: A dictionary with the keys "ranking", "tier" and "percentage".
    """
    return rank_data(artist_name, db)



@router.get("/loyalty", response_model=int)
def get_listener_loyalty(listener_name: str, user: CurrentUser, db: Session = Depends(get_db)) -> int:
    """
    Retrieve the loyalty metric of a listener related to the artist authenticated. 
    The listener_name will be the only parameter.

    An exception will be raised if there is no authorization token or if the one given does not belong to an artist.

    Args:
        listener_name (str): The listener username.

    Returns:
        int: Loyalty points of the listener related to the artist.
    """
    return loyalty_points(get_artist_by_username(db, user.username), get_listener_by_username(db, listener_name), db)