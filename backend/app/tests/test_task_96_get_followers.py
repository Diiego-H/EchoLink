from fastapi.testclient import TestClient
from main import app
from core.config import get_db
from tests.utils import create_random_auth_artist, create_random_listener
from crud.listener import follow_artist 
client = TestClient(app)

def test_get_artists_followers():
    db = next(get_db())

    # Create two random users
    artist = create_random_auth_artist(db)
    listener1 = create_random_listener(db)
    listener2 = create_random_listener(db)
    listener3 = create_random_listener(db)
    listener4 = create_random_listener(db)



    # Follow the artist
    follow_artist(db, listener1, artist.username)
    follow_artist(db, listener2, artist.username)
    follow_artist(db, listener3, artist.username)
    follow_artist(db, listener4, artist.username)


    # Call the /followers endpoint
    response = client.get(
        f"/metrics/followers?artist_name={artist.username}",
    )

    # Assert the response status code
    assert response.status_code == 200

    # Assert the response contains the correct data
    # Assert the response contains a valid float value
    engagement_rate = response.json()
    assert isinstance(engagement_rate, int)
    assert engagement_rate == 4


    # Clean up the database
    db.delete(artist)
    db.delete(listener1.user)
    db.delete(listener2.user)
    db.delete(listener4.user)
    db.delete(listener3.user)
    db.commit()