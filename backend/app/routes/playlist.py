from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from pytest import Session
from core.config import get_db
from core.security import CurrentUser, OptionalCurrentUser
from typing import List
from models.playlist import Playlist, PlaylistInput, PlaylistOutput, PlaylistUpdate
from crud.playlist import (
    get_playlist_by_id as get_playlist_by_id_crud,
    get_playlists_by_username as get_playlists_by_username_crud,
    create_playlist as create_playlist_crud,
    update_playlist as update_playlist_crud,
    delete_playlist as delete_playlist_crud,
    add_song_to_playlist as add_song_to_playlist_crud,
    remove_song_from_playlist as remove_song_from_playlist_crud,
    reorder_songs_in_playlist as reorder_songs_in_playlist_crud
)

router = APIRouter()

def transform_playlist_to_output(playlist: Playlist) -> PlaylistOutput:
    return PlaylistOutput(
        playlist_id=playlist.playlist_id,
        name=playlist.name,
        description=playlist.description,
        visibility=playlist.visibility,
        username=playlist.user.username,
        songs=[{"song_id": song.song_id} for song in playlist.songs]
    )

@router.get("/{playlist_id}", response_model=PlaylistOutput)
def get_playlist_by_id(
    playlist_id: int,
    current_user: OptionalCurrentUser,
    db: Session = Depends(get_db)
):
    """
    Retrieve a playlist by ID.
    """
    playlist = get_playlist_by_id_crud(db, playlist_id, current_user.id if current_user else None)
    return transform_playlist_to_output(playlist)

@router.get("/user/{username}", response_model=List[PlaylistOutput])
def get_playlists_by_username(
    username: str,
    current_user: OptionalCurrentUser,
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of playlists by username.
    """
    playlists = get_playlists_by_username_crud(db, username, current_user.id if current_user else None)
    return [transform_playlist_to_output(playlist) for playlist in playlists]

@router.post("/", response_model=PlaylistOutput)
def create_playlist(
    playlist_data: PlaylistInput,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    """
    Create a new playlist.
    """
    playlist = create_playlist_crud(db, playlist_data, current_user.id)
    return transform_playlist_to_output(playlist)

@router.put("/{playlist_id}", response_model=PlaylistOutput)
def update_playlist(
    playlist_id: int,
    update_data: PlaylistUpdate,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    """
    Update an existing playlist.
    """
    playlist = update_playlist_crud(db, playlist_id, update_data, current_user.id)
    return transform_playlist_to_output(playlist)

@router.delete("/{playlist_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_playlist(
    playlist_id: int,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    """
    Delete a playlist by ID.
    """
    delete_playlist_crud(db, playlist_id, current_user.id)
    return None

@router.post("/{playlist_id}/song/{song_id}", response_model=PlaylistOutput)
def add_song_to_playlist(
    playlist_id: int,
    song_id: int,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    """
    Add a song to a playlist.
    """
    playlist = add_song_to_playlist_crud(db, playlist_id, song_id, current_user.id)
    return transform_playlist_to_output(playlist)

@router.delete("/{playlist_id}/song/{song_id}", response_model=PlaylistOutput)
def remove_song_from_playlist(
    playlist_id: int,
    song_id: int,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    """
    Remove a song from a playlist.
    """
    playlist = remove_song_from_playlist_crud(db, playlist_id, song_id, current_user.id)
    return transform_playlist_to_output(playlist)

class ReorderSongsRequest(BaseModel):
    song_ids: List[int]  # Ensure this is a list of integers

@router.put("/{playlist_id}/reorder", response_model=PlaylistOutput)
def reorder_songs_in_playlist(
    playlist_id: int,
    reorder_request: ReorderSongsRequest,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    """
    Reorder songs in a playlist.
    """
    playlist = reorder_songs_in_playlist_crud(db, playlist_id, reorder_request.song_ids, current_user.id)
    return transform_playlist_to_output(playlist)
