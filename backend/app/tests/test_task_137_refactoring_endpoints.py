from fastapi.testclient import TestClient
from main import app
from core.config import get_db
from tests.utils import create_random_auth_listener, create_random_auth_artist



client = TestClient(app)

def test_get_artists_alphabet():
    db = next(get_db())

    # Create random artists
    artist1_user = create_random_auth_artist(db)
    artist2_user = create_random_auth_artist(db)

    # Call the endpoint
    response = client.get(
        "/artists/",
        headers={"Authorization": f"Bearer {artist1_user.token}"}
    )

    # Assert the response status code
    assert response.status_code == 200

    # Assert the response is sorted alphabetically by username
    artists = response.json()
    assert len(artists) == 2

    # Assert the required fields are present in the response
    for artist in artists:
        assert "rank_data" in artist
        assert "can_ask" in artist
        assert "is_following" in artist


    

    # Clean up the database
    db.delete(artist1_user)
    db.delete(artist2_user)
    db.commit()


def test_get_artists_engagement():
    db = next(get_db())

    # Create random artists
    artist1_user = create_random_auth_artist(db)
    artist2_user = create_random_auth_artist(db)

    # Call the endpoint
    response = client.get(
        "/artists/engagement",
        headers={"Authorization": f"Bearer {artist1_user.token}"}
    )

    # Assert the response status code
    assert response.status_code == 200

    # Assert the response is sorted alphabetically by username
    artists = response.json()
    assert len(artists) == 2

    # Assert the required fields are present in the response
    for artist in artists:
        assert "rank_data" in artist
        assert "can_ask" in artist
        assert "is_following" in artist


    

    # Clean up the database
    db.delete(artist1_user)
    db.delete(artist2_user)
    db.commit()

def test_get_artists_followers():
    db = next(get_db())

    # Create random artists
    artist1_user = create_random_auth_artist(db)
    artist2_user = create_random_auth_artist(db)

    # Call the endpoint
    response = client.get(
        "/artists/followers",
        headers={"Authorization": f"Bearer {artist1_user.token}"}
    )

    # Assert the response status code
    assert response.status_code == 200

    # Assert the response is sorted alphabetically by username
    artists = response.json()
    assert len(artists) == 2

    # Assert the required fields are present in the response
    for artist in artists:
        assert "rank_data" in artist
        assert "can_ask" in artist
        assert "is_following" in artist


    # Clean up the database
    db.delete(artist1_user)
    db.delete(artist2_user)
    db.commit()


def test_get_sorted_artists_preferences():
    db = next(get_db())

    # Create a random user and some artists
    listener_user = create_random_auth_listener(db)
    artist1_user = create_random_auth_artist(db)
    artist2_user = create_random_auth_artist(db)


    # Call the endpoint
    response = client.get(
        "/listeners/preferences",
        headers={"Authorization": f"Bearer {listener_user.token}"}
    )

    # Assert the response status code
    assert response.status_code == 200

    # Assert the response contains the sorted list of artists
    artists = response.json()
    assert len(artists) == 2

    # Assert the required fields are present in the response
    for artist in artists:
        assert "rank_data" in artist
        assert "can_ask" in artist
        assert "is_following" in artist

    # Clean up the database
    db.delete(listener_user)
    db.delete(artist1_user)
    db.delete(artist2_user)
    db.commit()
