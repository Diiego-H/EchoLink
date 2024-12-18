from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from core.config import get_db
from core.security import get_current_user, CurrentUser
from crud.song import get_song_by_id as get_song_by_id_crud, \
    get_all_songs as get_all_songs_crud, \
    create_song as create_song_crud, \
    update_song as update_song_crud, \
    delete_song as delete_song_crud, \
    is_artist_owner_song as is_artist_owner_song_crud, \
    is_user_artist as is_user_artist_crud, \
    get_recommendations as get_recommendations_crud, \
    sort_songs_alphabetically as sort_songs_alphabetically_crud, \
    sort_songs_by_release_date as sort_songs_by_release_date_crud, \
    get_songs_by_artist_engagement_score as get_songs_by_artist_engagement_score_crud, \
    get_songs_by_artist_priority as get_songs_by_artist_priority_crud
from crud.artist import get_artist_by_user_id
import models.song as song_model
import models.user as user_model
from typing import List

router = APIRouter()

# GET /songs/recommendations -> Get song recommendations
@router.get("/recommendations", response_model=List[song_model.SongOutput])
def get_recommendations(
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    """
    Recommend 10 songs for the authenticated listener.
    """
    recommendations = get_recommendations_crud(db, current_user)
    return [transform_song_to_output(song) for song in recommendations]

# GET /songs -> Retrieve all songs
@router.get("/", response_model=list[song_model.SongOutput])
async def retrieve_all_songs(
    db: Session = Depends(get_db)
):
    return get_all_songs_crud(db)

# GET /songs/{song_id} -> Retrieve song by ID
@router.get("/{song_id}", response_model=song_model.SongOutput)
async def retrieve_song_by_id(
    song_id: int,
    db: Session = Depends(get_db)
):
    return get_song_by_id_crud(db, song_id)

# GET /songs/sorted/alphabetically
@router.get("/sorted/alphabetically", response_model=list[song_model.SongOutput])
async def sort_songs_alphabetically(
    db: Session = Depends(get_db)
):
    return sort_songs_alphabetically_crud(db)

# GET /songs/sorted/release_date
@router.get("/sorted/release_date", response_model=list[song_model.SongOutput])
async def sort_songs_by_release_date(
    db: Session = Depends(get_db)
):
    return sort_songs_by_release_date_crud(db)

# GET /songs/sorted/engagement_score
@router.get("/sorted/engagement_score", response_model=list[song_model.SongOutput])
async def get_songs_by_artist_engagement_score(
    db: Session = Depends(get_db)
):
    return get_songs_by_artist_engagement_score_crud(db)

# GET /songs/sorted/priority
@router.get("/sorted/priority", response_model=list[song_model.SongOutput])
async def get_songs_by_artist_priority(
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    return get_songs_by_artist_priority_crud(db, current_user.id)

# POST /songs -> Create a song
@router.post("/", response_model=song_model.SongOutput)
async def add_song(
    song_input: song_model.SongInput,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    is_user_artist_crud(db, current_user.id)

    return create_song_crud(db, song_input)

# PUT /songs/{song_id} -> Update a song
@router.put("/{song_id}", response_model=song_model.SongOutput)
async def update_song(
    song_id: int,
    song_update: song_model.SongInput,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    is_user_artist_crud(db, current_user.id)
    artist = get_artist_by_user_id(db, current_user.id)
    is_artist_owner_song_crud(db, artist.artist_id, song_id)

    return update_song_crud(db, song_id, song_update)

# DELETE /songs/{song_id} -> Delete a song
@router.delete("/{song_id}", status_code=status.HTTP_200_OK)
async def delete_song(
    song_id: int,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    is_user_artist_crud(db, current_user.id)
    artist = get_artist_by_user_id(db, current_user.id)
    is_artist_owner_song_crud(db, artist.artist_id, song_id)
    
    delete_song_crud(db, song_id)
    return {"message": "Song deleted successfully"}

def transform_song_to_output(song: song_model.Song):
    return song_model.SongOutput(
        song_id=song.song_id,
        title=song.title,
        album=song.album,
        genre=song.genre,
        release_date=song.release_date,
        artist_name=song.artist.name,
        sources=song.source_urls
    )

