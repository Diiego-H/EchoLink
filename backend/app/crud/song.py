from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.song import Song, SongInput, SongOutput, SongSource
from models.artist import Artist
from models.user import ListenerArtistLink, User, RoleEnum
from crud.listener import get_followed_artists
from crud.artist import get_artist_by_username
from crud.listener import get_listener_by_user_id, get_songs_id_in_playlist
from crud.artist import get_other_artists
from metrics.artists import get_all_artists_with_rank_data
import random

# Helper function to get a song or raise an error
def _get_song_or_error(db: Session, song_id: int) -> Song:
    song = db.query(Song).filter(Song.song_id == song_id).first()
    if song is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Song not found")
    return song

# Get song by ID
def get_song_by_id(db: Session, song_id: int) -> SongOutput:
    song = _get_song_or_error(db, song_id)
    
    return SongOutput(
        song_id=song.song_id,
        title=song.title,
        album=song.album,
        genre=song.genre,
        release_date=song.release_date,
        artist_name=song.artist.user.username,
        sources=song.source_urls
    )

# Get songs by artist_id
def get_songs_by_artist_id(db: Session, artist_id: int):
    return db.query(Song).filter(Song.artist_id == artist_id).all()

# Get artist by song id
def get_artist_by_song_id(db: Session, song_id: int) -> Artist:
    song = db.query(Song).filter(Song.song_id == song_id).first()
    if song is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Song not found")
    return song.artist

# Get artist id by song id
def get_artist_id_by_song_id(db: Session, followed_artists: list, user_id: int) -> int:
    playlist_songs = get_songs_id_in_playlist(db, user_id)
    playlist_artists = []
    for song in playlist_songs:
        artist = get_artist_by_song_id(db, song)
        if artist.artist_id in followed_artists:
            continue
        elif artist.artist_id not in playlist_artists:
            playlist_artists.append(artist.artist_id)

    return playlist_artists

# Get all songs
def get_all_songs(db: Session) -> list[SongOutput]:
    songs = db.query(Song).all()
    return [
        SongOutput(
            song_id=song.song_id,
            title=song.title,
            album=song.album,
            genre=song.genre,
            release_date=song.release_date,
            artist_name=song.artist.user.username,
            sources=song.source_urls
        )
        for song in songs
    ]

# Create a song
def create_song(db: Session, song_data: SongInput) -> SongOutput:
    artist = get_artist_by_username(db, song_data.artist_name)
    song = Song(
        title=song_data.title,
        album=song_data.album,
        genre=song_data.genre,
        release_date=song_data.release_date,
        artist_id=artist.artist_id
    )

    db.add(song)
    db.commit()
    db.refresh(song)

    # Add song sources (now song_id is assigned)
    song.sources = [SongSource(song_id=song.song_id, source_url=str(url)) for url in song_data.sources]

    return SongOutput(
        song_id=song.song_id,
        title=song.title,
        album=song.album,
        genre=song.genre,
        release_date=song.release_date,
        artist_name=artist.user.username,
        sources=song.source_urls
    )

# Update a song
def update_song(db: Session, song_id: int, song_data: SongInput) -> SongOutput:
    song = db.query(Song).filter(Song.song_id == song_id).first()
    if song is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Song not found")
    
    # Clear existing sources
    db.query(SongSource).filter(SongSource.song_id == song.song_id).delete()
    db.commit()
    
    artist = get_artist_by_username(db, song_data.artist_name)
    song.title = song_data.title
    song.album = song_data.album
    song.genre = song_data.genre
    song.release_date = song_data.release_date
    song.artist_id = artist.artist_id

    # Update with new sources
    song.sources = [SongSource(song_id=song.song_id, source_url=str(url)) for url in song_data.sources]

    db.commit()
    db.refresh(song)

    return SongOutput(
        song_id=song.song_id,
        title=song.title,
        album=song.album,
        genre=song.genre,
        release_date=song.release_date,
        artist_name=artist.user.username,
        sources=song.source_urls
    )

# Delete a song
def delete_song(db: Session, song_id: int):
    song = _get_song_or_error(db, song_id)
    song_output = SongOutput(
        song_id=song.song_id,
        title=song.title,
        album=song.album,
        genre=song.genre,
        release_date=song.release_date,
        artist_name=song.artist.user.username,
        sources = []
    )
    db.delete(song)
    db.commit()

    return song_output

# Check if an artist is the owner of a song
def is_artist_owner_song(db: Session, artist_id: int, song_id: int):
    song = _get_song_or_error(db, song_id)
    if song.artist_id != artist_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this song")
        
# Check of a user is an artist.
def is_user_artist(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user.role != RoleEnum.artist:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not an artist") 

def get_recommendations(db: Session, user: User) -> list[Song]:
    # Check if the user is a listener
    listener = get_listener_by_user_id(db, user.id)
    if not listener:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This user is not a listener.")
    
    # Step 0: Check if database has at least 10 songs, otherwise return all songs
    song_count = db.query(Song).count()
    if song_count < 10:
        return db.query(Song).all()

    # Step 1: Get songs by followed artists
    followed_artists = (
        db.query(Artist.artist_id)
        .join(ListenerArtistLink, ListenerArtistLink.artist_id == Artist.artist_id)
        .filter(ListenerArtistLink.listener_id == listener.listener_id)
        .all()
    )
    followed_songs = (
        db.query(Song)
        .filter(Song.artist_id.in_([artist.artist_id for artist in followed_artists]))
        .all()
    )

    # If there are 30 or more songs, pick 10 at random
    if len(followed_songs) >= 30:
        return random.sample(followed_songs, 10)

    # Step 2: Add songs with the listener's preferred genre
    genres = db.query(Song.genre).filter(Song.artist_id.in_([artist.artist_id for artist in followed_artists])).distinct().all()
    genres = [genre[0] for genre in genres]
    genres_songs = (
        db.query(Song)
        .filter(Song.genre.in_(genres))
        .all()
    )

    combined_list = list(set(followed_songs + genres_songs))

    # If the combined list has 30 or more songs, pick 10 at random
    if len(combined_list) >= 30:
        return random.sample(combined_list, 10)

    # Step 3: Handle small lists
    selected_songs = random.sample(combined_list, min(5, len(combined_list)))

    # Add random songs from the database excluding already selected ones
    remaining_songs = (
        db.query(Song)
        .filter(~Song.song_id.in_([song.song_id for song in combined_list]))
        .all()
    )
    additional_songs = random.sample(remaining_songs, 10 - len(selected_songs))
    return selected_songs + additional_songs

  # Sort songs alphabetically
def sort_songs_alphabetically(db: Session, ascending: bool = True) -> list[SongOutput]:
    """
    Retrieve and sort all songs alphabetically by title.

    Args:
    - db: Database session
    - ascending: Sort in ascending order if True, descending order if False

    Returns:
    - List of SongOutput objects
    """
    order = Song.title.asc() if ascending else Song.title.desc()
    songs = db.query(Song).order_by(order).all()

    return [
        SongOutput(
            song_id=song.song_id,
            title=song.title,
            album=song.album,
            genre=song.genre,
            release_date=song.release_date,
            artist_name=song.artist.user.username,
            sources=song.source_urls
        )
        for song in songs
    ]

# Sort songs by release date
def sort_songs_by_release_date(db: Session, ascending: bool = True) -> list[SongOutput]:
    """
    Retrieve and sort all songs by release date.

    Args:
    - db: Database session
    - ascending: Sort in ascending order if True, descending order if False

    Returns:
    - List of SongOutput objects
    """
    order = Song.release_date.asc() if ascending else Song.release_date.desc()
    songs = db.query(Song).order_by(order).all()

    return [
        SongOutput(
            song_id=song.song_id,
            title=song.title,
            album=song.album,
            genre=song.genre,
            release_date=song.release_date,
            artist_name=song.artist.user.username,
            sources=song.source_urls
        )
        for song in songs
    ]

def get_songs_by_artist_engagement_score(db: Session, ascending: bool = True) -> list[SongOutput]:
    """
    Retrieve all songs and sort them by the engagement score of the artist.

    Args:
    - db: Database session
    - ascending: Boolean flag to indicate if sorting should be ascending (True) or descending (False).

    Returns:
    - List of SongOutput objects
    """

    # Get all artists with rank data
    artists = get_all_artists_with_rank_data(db)

    # Create a dictionary to hold songs for each priority tier
    tiered_songs = {0: [], 1: [], 2: [], 3: [], 4: []}

    # Iterate through artists and add their songs to the appropriate tier
    for artist in artists:
        tier = artist.rank_data["tier"]
        artist = get_artist_by_username(db, artist.username)
        songs = get_songs_by_artist_id(db, artist.artist_id)

        # Add songs to the appropriate tier
        tiered_songs[tier].extend(songs)

    # Shuffle songs within each tier
    for tier_songs in tiered_songs.values():
        random.shuffle(tier_songs)

    # Define the order of the tiers
    tier_order = [0, 1, 2, 3, 4] if ascending else [4, 3, 2, 1, 0]

    # Create a list of songs sorted by tier
    sorted_songs = []
    for tier in tier_order:
        sorted_songs.extend(tiered_songs[tier])

    return [
        SongOutput(
            song_id=song.song_id,
            title=song.title,
            album=song.album,
            genre=song.genre,
            release_date=song.release_date,
            artist_name=song.artist.user.username,
            sources=song.source_urls
        )
        for song in sorted_songs
    ]

def get_songs_by_artist_priority(db: Session, user_id: int) -> list[SongOutput]:
    """
    Retrieve songs ordered by artist priority:
    1. Songs from artists followed by the user.
    2. Songs from artists that have at least one song added to the user's playlist.
    3. Songs from other artists.

    Args:
    - db: Database session
    - user_id: The user ID to identify the followed artists and playlists
    - ascending: Whether to sort in ascending or descending order of priority

    Returns:
    - List of SongOutput objects
    """
    # Get the listener by user ID
    listener = get_listener_by_user_id(db, user_id)

    # Initialize the lists for each priority tier
    followed_songs = []
    playlist_songs = []
    other_songs = []

    # Get the ids of artists followed by the user
    followed_artists = get_followed_artists(db, listener.listener_id)
    playlist_artists = get_artist_id_by_song_id(db, followed_artists, listener.user_id)
    other_artists = get_other_artists(db, followed_artists, playlist_artists)

    for artist in followed_artists:
        followed_songs.extend(get_songs_by_artist_id(db, artist))

    for artist in playlist_artists:
        playlist_songs.extend(get_songs_by_artist_id(db, artist))

    for artist in other_artists:
        other_songs.extend(get_songs_by_artist_id(db, artist))

    # Shuffle the songs within each tier
    random.shuffle(followed_songs)
    random.shuffle(playlist_songs)
    random.shuffle(other_songs)

    songs = followed_songs + playlist_songs + other_songs

    return [
        SongOutput(
            song_id=song.song_id,
            title=song.title,
            album=song.album,
            genre=song.genre,
            release_date=song.release_date,
            artist_name=song.artist.user.username,
            sources=song.source_urls
        )
        for song in songs
    ]







