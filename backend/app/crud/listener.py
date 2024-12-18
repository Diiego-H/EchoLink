from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.listener import Listener
from models.user import ListenerArtistLink, User
from crud.artist import get_artist_by_username, get_artists
from crud.playlist import get_playlists_by_user_id, get_songs_in_playlist

# Get listener by user_id
def get_listener_by_user_id(db: Session, user_id: int) -> Listener:
    return db.query(Listener).filter(Listener.user_id == user_id).first()

# Get listener by listener_id
def get_listener_by_listener_id(db: Session, listener_id: int) -> Listener:
    return db.query(Listener).filter(Listener.listener_id == listener_id).first()

# Create listener
def create_listener(db: Session, user: User) -> Listener:
    # Check if a listener already exists for this user
    if get_listener_by_user_id(db, user.id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This user is already a listener.")

    # Create a new listener
    listener = Listener(user_id=user.id)

    # Save to the database
    db.add(listener)
    db.commit()
    db.refresh(listener)

    return listener

# Get listeners
def get_all_listeners(db: Session):
    return db.query(Listener).all()

# Get listener by username
def get_listener_by_username(db: Session, username: str) -> Listener:
    # Get user by username
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    
    # Get listener by user_id
    listener = get_listener_by_user_id(db, user.id)
    if not listener:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This user is not a listener.")
    
    return listener


def check_follow(db: Session, listener: Listener, artist_username: str) -> bool:
    artist = get_artist_by_username(db, artist_username)
    return db.query(ListenerArtistLink).filter(
        ListenerArtistLink.listener_id == listener.listener_id,
        ListenerArtistLink.artist_id == artist.artist_id
    ).first() is not None


# Follow an artist
def follow_artist(db: Session, listener: Listener, artist_username: str) -> ListenerArtistLink:
    artist = get_artist_by_username(db, artist_username)

    # Check if the listener is already following the artist
    existing_follow = db.query(ListenerArtistLink).filter(
        ListenerArtistLink.listener_id == listener.listener_id,
        ListenerArtistLink.artist_id == artist.artist_id
    ).first()
    if existing_follow:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The listener follows the artist.")

    # Create the follow link
    follow_link = ListenerArtistLink(listener_id=listener.listener_id, artist_id=artist.artist_id)
    db.add(follow_link)
    db.commit()
    db.refresh(follow_link)

    return follow_link

# Unfollow an artist
def unfollow_artist(db: Session, listener: Listener, artist_username: str):
    artist = get_artist_by_username(db, artist_username)

    # Check if the listener is following the artist
    follow = db.query(ListenerArtistLink).filter(
        ListenerArtistLink.listener_id == listener.listener_id,
        ListenerArtistLink.artist_id == artist.artist_id
    ).first()
    if not follow:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The listener does not follow the artist.")

    # Delete the follow link
    db.delete(follow)
    db.commit()

def get_followed_artists(db: Session, listener_id: int):

    # Query the ListenerArtistLink to get the artist_ids for the given user
    followed_artists_ids = db.query(ListenerArtistLink.artist_id).filter(
        ListenerArtistLink.listener_id == listener_id
    ).all()

    # Return a list of artist IDs (flatten the result)
    return [artist_id for artist_id, in followed_artists_ids]

def get_songs_id_in_playlist(db: Session, user_id: int):

    playlists = get_playlists_by_user_id(db, user_id)

    # Get all the songs in the playlists
    songs = []
    for playlist in playlists:
        songs += get_songs_in_playlist(db, playlist.playlist_id)

    return songs

# Get a sorted list of artists based on:
# - If the listener can ask a question to the artist
# - If the listener follows the artist
# - Other criteria

def get_sorted_artists(db: Session, user_id: int, limit: int = 6):
    from crud.question import can_question
    
    if type(user_id) is User:
        user_id = user_id.id

    listener = get_listener_by_user_id(db, user_id)

    # Get all artists
    artists = get_artists(db)
    prioritized_artists = []

    for artist in artists:
        if can_question(db, listener, artist):
            priority = 0

        elif check_follow(db, listener, artist.user.username):
            priority = 1

        else:
            priority = 2

        prioritized_artists.append((priority, artist))

    # Sort the artists based on the priority
    prioritized_artists.sort(key=lambda x: x[0])
    sorted_artists = [artist for _, artist in prioritized_artists[:limit]]

    return sorted_artists