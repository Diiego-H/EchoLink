from sqlalchemy.orm import Session
from models.playlist import Playlist, PlaylistInput, PlaylistUpdate, playlist_songs
from typing import List, Optional
from models.user import User
from sqlalchemy import func, insert, update, delete

# Create a new playlist
def create_playlist(db: Session, playlist_data: PlaylistInput, user_id: int) -> Playlist:
    # Check if the playlist name already exists for the user
    existing_playlist = db.query(Playlist).filter(Playlist.name == playlist_data.name, Playlist.user_id == user_id).first()
    if existing_playlist:
        raise ValueError("Playlist with this name already exists")

    # Create a new playlist
    new_playlist = Playlist(
        name=playlist_data.name,
        description=playlist_data.description,
        visibility=playlist_data.visibility,
        user_id=user_id
    )
    db.add(new_playlist)
    db.commit()
    db.refresh(new_playlist)
    return new_playlist

# Retrieve all playlists by user ID
def get_playlists_by_user_id(db: Session, user_id: int) -> List[Playlist]:
    return db.query(Playlist).filter(Playlist.user_id == user_id).all()

# Get all the songs in a playlist
def get_songs_in_playlist(db: Session, playlist_id: int) -> List[int]:
    playlist = db.query(Playlist).filter(Playlist.playlist_id == playlist_id).first()

    if not playlist:
        raise ValueError("Playlist not found")
    
    return [song.song_id for song in playlist.songs]


# Retrieve a playlist by ID and check ownership and visibility
def get_playlist_by_id(db: Session, playlist_id: int, user_id: int) -> Optional[Playlist]:
    playlist = db.query(Playlist).filter(Playlist.playlist_id == playlist_id).first()

    if not playlist:
        raise ValueError("Playlist not found")

    if playlist.user_id != user_id and playlist.visibility.value == "private":
        raise ValueError("User does not have permission to view this playlist")

    return playlist

# Retrieve all playlists by username and check ownership or playlist visibility
def get_playlists_by_username(db: Session, username: str, user_id: int) -> List[Playlist]:
    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise ValueError("User not found")

    playlists = db.query(Playlist).filter(Playlist.user_id == user.id).all()

    if user.id != user_id:
        playlists = [playlist for playlist in playlists if playlist.visibility.value == "public"]

    return playlists

# Update an existing playlist
def update_playlist(db: Session, playlist_id: int, update_data: PlaylistUpdate, user_id: int) -> Optional[Playlist]:
    playlist = db.query(Playlist).filter(Playlist.playlist_id == playlist_id).first()

    if playlist.user_id != user_id:
        raise ValueError("User does not have permission to update this playlist")

    if playlist:
        update_data = update_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(playlist, key, value)

        db.commit()
        db.refresh(playlist)
    
    return playlist

# Delete a playlist
def delete_playlist(db: Session, playlist_id: int, user_id: int) -> bool:
    playlist = db.query(Playlist).filter(Playlist.playlist_id == playlist_id).first()

    if playlist.user_id != user_id:
        raise ValueError("User does not have permission to delete this playlist")

    if playlist:
        db.delete(playlist)
        db.commit()
        return True
    return False

def add_song_to_playlist(db: Session, playlist_id: int, song_id: int, user_id: int) -> Playlist:
    # Retrieve the playlist and check ownership
    playlist = db.query(Playlist).filter(Playlist.playlist_id == playlist_id).first()
    if not playlist:
        raise ValueError("Playlist not found.")
    if playlist.user_id != user_id:
        raise ValueError("User does not have permission to modify this playlist.")

    # Check if the song is already in the playlist
    if any(song.song_id == song_id for song in playlist.songs):
        raise ValueError("This song is already in the playlist.")

    # Calculate the next order value
    max_order = db.query(func.coalesce(func.max(playlist_songs.c.order), 0)).filter(playlist_songs.c.playlist_id == playlist_id).scalar()
    next_order = max_order + 1

    # Add the association with the calculated order
    stmt = insert(playlist_songs).values(playlist_id=playlist_id, song_id=song_id, order=next_order)
    db.execute(stmt)
    db.commit()
    return playlist

def remove_song_from_playlist(db: Session, playlist_id: int, song_id: int, user_id: int) -> Playlist:
    # Retrieve the playlist and check ownership
    playlist = db.query(Playlist).filter(Playlist.playlist_id == playlist_id).first()
    if not playlist:
        raise ValueError("Playlist not found.")
    if playlist.user_id != user_id:
        raise ValueError("User does not have permission to modify this playlist.")

    # Check if the song exists in the playlist
    song_entry = (
        db.query(playlist_songs)
        .filter(playlist_songs.c.playlist_id == playlist_id, playlist_songs.c.song_id == song_id)
        .first()
    )
    if not song_entry:
        raise ValueError("Song not found in playlist.")

    # Remove song from playlist
    db.execute(
        delete(playlist_songs)
        .where(playlist_songs.c.playlist_id == playlist_id, playlist_songs.c.song_id == song_id)
    )

    # Adjust order for remaining songs
    remaining_songs = (
        db.query(playlist_songs)
        .filter(playlist_songs.c.playlist_id == playlist_id)
        .order_by(playlist_songs.c.order)
        .all()
    )
    for index, song in enumerate(remaining_songs, start=1):
        db.execute(
            update(playlist_songs)
            .where(playlist_songs.c.playlist_id == playlist_id, playlist_songs.c.song_id == song.song_id)
            .values(order=index)
        )

    db.commit()
    db.refresh(playlist)
    return playlist

def reorder_songs_in_playlist(db: Session, playlist_id: int, new_order: List[int], user_id: int) -> Playlist:
    # Retrieve the playlist and check ownership
    playlist = db.query(Playlist).filter(Playlist.playlist_id == playlist_id).first()
    if not playlist:
        raise ValueError("Playlist not found.")
    if playlist.user_id != user_id:
        raise ValueError("User does not have permission to modify this playlist.")

    # Validate new order
    # Extract current song IDs from the playlist
    current_song_ids = (
        db.query(playlist_songs.c.song_id)
        .filter(playlist_songs.c.playlist_id == playlist_id)
        .all()
    )
    current_song_ids = [song_id for (song_id,) in current_song_ids]

    if sorted(current_song_ids) != sorted(new_order):
        raise ValueError("New order is invalid. It must include all songs in the playlist exactly once.")

    # Reorder the songs
    for index, song_id in enumerate(new_order, start=1):
        db.execute(
            update(playlist_songs)
            .where(playlist_songs.c.playlist_id == playlist_id, playlist_songs.c.song_id == song_id)
            .values(order=index)
        )
    
    db.commit()
    db.refresh(playlist)
    return playlist

