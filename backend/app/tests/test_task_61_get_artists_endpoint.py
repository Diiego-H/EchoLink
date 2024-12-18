from .utils import get_db, create_user, create_listener
from models.user import UserInput, RoleEnum
from crud.artist import get_all_artists

# Test the `get_all_artists` function
def test_get_all_artists():
    session = next(get_db())

    # Create test users: 1 artist and 1 non-artist
    artist_input = UserInput(username="artist1", email="artist1@artist1.com", password="artist_pwd", role=RoleEnum.artist, genre="Rock")
    artist = create_user(session, artist_input)
    listener = create_listener(session)

    # Call the function to get all artists
    artists = get_all_artists(session)

    # Verify that the result contains only the artist user and not the non-artist user
    assert len(artists) == 1
    assert artists[0].username == "artist1"
    assert artists[0].role == RoleEnum.artist

    # Verify that the artist's genre is correctly returned
    assert artists[0].genre == "Rock"

    # Delete data created
    session.delete(artist)
    session.delete(listener.user)
    session.commit()