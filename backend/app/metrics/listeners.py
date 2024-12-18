from models.listener import Listener
from models.playlist import Playlist
from models.question import Question, ResponseEnum
from models.artist import Artist
from pytest import Session
from crud.listener import check_follow, get_all_listeners, get_sorted_artists, get_listener_by_user_id
from crud.artist import get_artist_by_username


def loyalty_points(artist: Artist, listener: Listener, db: Session) -> int:
    # Check if the listener follows the artist
    follow_score = 5000 if check_follow(db, listener, artist.user.username) else 0

    # Questions from the listener to the artist
    questions = db.query(Question).filter(Question.artist_id == artist.artist_id, 
                                          Question.listener_id == listener.listener_id).all()
    
    # Calculate the score based on the number of questions (small, increase the value with answer/reject rate)
    question_score = 20 * len(questions)

    # Answered questions give more points
    answer_score = 1000 * sum(1 for question in questions if question.response_status == ResponseEnum.answered)

    # Rejected questions reduce the score
    reject_score = -200 * sum(1 for question in questions if question.response_status == ResponseEnum.rejected)

    # Playlists with artist's songs give points (based on the % of songs of the artist)
    playlists = db.query(Playlist).filter(Playlist.user_id == listener.user_id).all()
    playlist_score = 0
    for playlist in playlists:
        artist_songs = sum(1 for song in playlist.songs if song.artist_id == artist.artist_id)
        if len(playlist.songs) > 0:
            playlist_score += 50 * artist_songs / len(playlist.songs)

    # Check if the listener's favorite genre matches the artist's genre
    genre_score = 100 if listener.user.genre == artist.user.genre else 0

    # Combine the scores
    loyalty_score = follow_score + question_score + answer_score + reject_score + playlist_score + genre_score

    # Return a score as an integer (minimum 1000)
    return 1000 + max(int(round(loyalty_score)), 0)


def loyalty_sorted_listeners(artist: Artist, db: Session) -> list:
    # Get all listeners and their loyalty points
    listeners = [[listener.user.username, loyalty_points(artist, listener, db)] for listener in get_all_listeners(db)]

    # Sort in descending order of loyalty points
    sorted_listeners = sorted(listeners, key=lambda x: x[1], reverse=True)

    return sorted_listeners


def get_listener_loyalty_data(artist: Artist, listener: Listener, db: Session):
    # Get listeners sorted by loyalty
    listeners = loyalty_sorted_listeners(artist, db)

    # Iterate through the list to get the listener ranking
    for i, (name, score) in enumerate(listeners, start=1):
        if name == listener.user.username:
            return {
                "ranking": i,
                "loyalty_points": score,
                "percentage": int(((i-1) / len(listeners)) * 100)
            }

    # This should not be reached
    raise RuntimeError("Could not determine the ranking for the listener.")


def get_preferences(db: Session, user_id: int):
    from models.artist import ArtistOutput
    from models.user import User
    from metrics.artists import rank_data
    from crud.question import can_question

    sorted_artist = get_sorted_artists(db, user_id)

    if type(user_id) is User:
        user_id = user_id.id

    listener = get_listener_by_user_id(db, user_id) if user_id else None



    return [
        ArtistOutput(
            username=artist.user.username,
            email=artist.user.email,
            genre=artist.user.genre,
            description=artist.user.description,
            visibility=artist.user.visibility,
            role=artist.user.role,
            image_url=artist.user.image_url,
            rank_data=rank_data(artist.user.username, db),
            can_ask=can_question(db, listener, get_artist_by_username(db, artist.user.username))if listener else False,
            is_following=check_follow(db, listener, artist.user.username) if listener else False
        )
        for artist in sorted_artist
    ]
