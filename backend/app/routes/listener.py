from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.listener import Listener
from crud.listener import follow_artist, unfollow_artist, check_follow
from core.config import get_db
from core.security import CurrentUser, OptionalCurrentUser
from metrics.listeners import get_preferences

router = APIRouter()

#Check if user follows an artist
@router.get("/follows/{artist_name}", status_code=200)
def check_follow_route(
    artist_name: str,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    # Check if the current user is a listener
    listener = db.query(Listener).filter(Listener.user_id == current_user.id).first()
    if not listener:
        raise HTTPException(status_code=400, detail="You must be a listener to follow an artist.")
    
    return {"follows": check_follow(db, listener, artist_name)}

# Get the artists sorted by preference
@router.get("/preferences", status_code=200)
def get_sorted_artists_route(
    current_user : OptionalCurrentUser,
    db: Session = Depends(get_db)
):
    # Return a list of artists sorted by preference
    return get_preferences(db, current_user.id if current_user is None else current_user)
    
# Follow an artist
@router.post("/follow/{artist_name}", status_code=200)
def follow_artist_route(
    artist_name: str,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    # Check if the current user is a listener
    listener = db.query(Listener).filter(Listener.user_id == current_user.id).first()
    if not listener:
        raise HTTPException(status_code=400, detail="You must be a listener to follow an artist.")
    
    return follow_artist(db, listener, artist_name)

# Unfollow an artist
@router.post("/unfollow/{artist_name}", status_code=200)
def unfollow_artist_route(
    artist_name: str,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    # Check if the current user is a listener
    listener = db.query(Listener).filter(Listener.user_id == current_user.id).first()
    if not listener:
        raise HTTPException(status_code=400, detail="You must be a listener to unfollow an artist.")

    unfollow_artist(db, listener, artist_name)
