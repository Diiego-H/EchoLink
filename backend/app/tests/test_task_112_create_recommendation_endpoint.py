from fastapi.testclient import TestClient
from crud.listener import follow_artist
from main import app
from core.config import get_db
from tests.utils import create_random_auth_listener, create_random_artist, create_random_song, random_lower_string
from crud.listener import get_listener_by_user_id

client = TestClient(app)

# Test all songs from same artist
def test_recommendations():
    db = next(get_db())

    # Create a listener
    listener_user = create_random_auth_listener(db)
    listener = get_listener_by_user_id(db, listener_user.id)

    # Create followed artists and their songs
    artist1 = create_random_artist(db)
    artist2 = create_random_artist(db)
    artist3 = create_random_artist(db)

    songIds = []
    for _ in range(20):
        song = create_random_song(db, artist1.name)
        songIds.append(song.song_id)
    for _ in range(20):
        song = create_random_song(db, artist2.name)
        songIds.append(song.song_id)
    for _ in range(20):
        song = create_random_song(db, artist3.name)
    
    # Follow the artists
    follow_artist(db, listener, artist1.name)
    follow_artist(db, listener, artist2.name)

    # Fetch recommendations
    response = client.get(
        "songs/recommendations",
        headers={"Authorization": f"Bearer {listener_user.token}"}
    )

    # Assert response
    assert response.status_code == 200
    recommendations = response.json()
    assert len(recommendations) == 10
    for song in recommendations:
        assert song["song_id"] in songIds

    # Cleanup
    db.delete(listener_user)
    db.delete(artist1.user)
    db.delete(artist2.user)
    db.delete(artist3.user)
    db.commit()

#Test followed artists have less than 30 songs so need to add same genre songs
def test_recommendations_same_genre():
    db = next(get_db())

    # Create a listener
    listener_user = create_random_auth_listener(db)
    listener = get_listener_by_user_id(db, listener_user.id)

    # Create followed artists and their songs
    artist1 = create_random_artist(db)
    artist2 = create_random_artist(db)
    artist3 = create_random_artist(db)

    genre1 = random_lower_string()
    genre2 = random_lower_string()

    songIds = []
    for _ in range(20):
        song = create_random_song(db, artist1.name, genre1)
        songIds.append(song.song_id)
    for _ in range(20):
        song = create_random_song(db, artist2.name, genre1)
        songIds.append(song.song_id)
    for _ in range(20):
        song = create_random_song(db, artist3.name, genre2)
    
    # Follow the artist
    follow_artist(db, listener, artist1.name)

    # Fetch recommendations
    response = client.get(
        "songs/recommendations",
        headers={"Authorization": f"Bearer {listener_user.token}"}
    )

    # Assert response
    assert response.status_code == 200
    recommendations = response.json()
    assert len(recommendations) == 10
    for song in recommendations:
        assert song["song_id"] in songIds

    # Cleanup
    db.delete(listener_user)
    db.delete(artist1.user)
    db.delete(artist2.user)
    db.delete(artist3.user)
    db.commit()

#Test followed artists and genre songs have less than 30 songs so need to add random songs
def test_recommendations_random():
    db = next(get_db())

    # Create a listener
    listener_user = create_random_auth_listener(db)
    listener = get_listener_by_user_id(db, listener_user.id)

    # Create followed artists and their songs
    artist1 = create_random_artist(db)
    artist2 = create_random_artist(db)
    artist3 = create_random_artist(db)

    genre1 = random_lower_string()
    genre2 = random_lower_string()

    for _ in range(10):
        create_random_song(db, artist1.name, genre1)
    for _ in range(10):
        create_random_song(db, artist2.name, genre1)
    for _ in range(20):
        create_random_song(db, artist3.name, genre2)
    
    # Follow the artist
    follow_artist(db, listener, artist1.name)

    # Fetch recommendations
    response = client.get(
        "songs/recommendations",
        headers={"Authorization": f"Bearer {listener_user.token}"}
    )

    # Assert response
    assert response.status_code == 200
    recommendations = response.json()
    assert len(recommendations) == 10

    # Cleanup
    db.delete(listener_user)
    db.delete(artist1.user)
    db.delete(artist2.user)
    db.delete(artist3.user)
    db.commit()

#Test less than 10 songs in database
def test_recommendations_less_than_10_songs():
    db = next(get_db())

    # Create a listener
    listener_user = create_random_auth_listener(db)

    # Create artist and their songs
    artist = create_random_artist(db)

    for _ in range(5):
        create_random_song(db, artist.name)

    # Fetch recommendations
    response = client.get(
        "songs/recommendations",
        headers={"Authorization": f"Bearer {listener_user.token}"}
    )

    # Assert response
    assert response.status_code == 200
    recommendations = response.json()
    assert len(recommendations) == 5

    # Cleanup
    db.delete(listener_user)
    db.delete(artist.user)
    db.commit()