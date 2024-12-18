from fastapi.testclient import TestClient
from main import app
from core.config import get_db
from tests.utils import create_random_auth_user
from crud.artist import create_artist

client = TestClient(app)

# Test for the /response_rate endpoint
def test_get_artist_reply_rate():
    db = next(get_db())

    # Create a random user
    user = create_random_auth_user(db)

    # Convert the user into an artist
    artist = create_artist(db, user)

    # Call the /response_rate endpoint
    response = client.get(
        f"/metrics/response_rate?artist_name={artist.name}",
    )

    # Assert the response status code
    assert response.status_code == 200

    # Assert the response contains a valid float value
    reply_rate = response.json()
    assert isinstance(reply_rate, float)

    # Clean up the database
    db.delete(artist)
    db.delete(user)
    db.commit()