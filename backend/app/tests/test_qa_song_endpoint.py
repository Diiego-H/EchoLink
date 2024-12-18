from tests.utils import get_session, get_client, create_random_auth_artist, create_random_auth_user, create_random_song, random_lower_string
from models.song import Song
from models.user import User

def test_create_song_successful():
    db = get_session()
    client = get_client()

    # Create an authenticated artist
    artist = create_random_auth_artist(db)
    song_data = {
        "title": random_lower_string(),
        "album": random_lower_string(),
        "genre": random_lower_string(),
        "release_date": "2024-11-26",
        "artist_name": artist.username
    }
    headers = {"Authorization": f"Bearer {artist.token}"}
    response = client.post("/songs/", json=song_data, headers=headers)

    assert response.status_code == 200
    song = response.json()
    assert song["title"] == song_data["title"]
    assert song["album"] == song_data["album"]
    assert song["genre"] == song_data["genre"]
    assert song["release_date"] == song_data["release_date"]
    assert song["artist_name"] == artist.username

    # Check if the song is created
    db_song = db.query(Song).filter(Song.title == song_data["title"]).first()
    assert db_song is not None

    # Clean up
    db.delete(db_song)
    db.delete(artist)
    db.commit()

    # Check if the song is deleted
    db_song = db.query(Song).filter(Song.title == song_data["title"]).first()
    assert db_song is None

    # Check if the user is deleted
    db_artist = db.query(User).filter(User.id == artist.id).first()
    assert db_artist is None

def test_create_song_as_no_artist():
    db = get_session()
    client = get_client()

    # Create an authenticated artist
    user = create_random_auth_user(db)
    song_data = {
        "title": random_lower_string(),
        "album": random_lower_string(),
        "genre": random_lower_string(),
        "release_date": "2024-11-26",
        "artist_name": user.username
    }
    headers = {"Authorization": f"Bearer {user.token}"}
    response = client.post("/songs/", json=song_data, headers=headers)

    assert response.status_code == 403
    assert response.json() == {"detail": "You are not an artist"}

    # Clean up
    db.delete(user)
    db.commit()

    # Check if the user is deleted
    db_artist = db.query(User).filter(User.id == user.id).first()
    assert db_artist is None

def test_delete_song_successful():
    db = get_session()
    client = get_client()

    # Create an authenticated artist
    artist = create_random_auth_artist(db)
    song = create_random_song(db, artist.username)
    headers = {"Authorization": f"Bearer {artist.token}"}
    response = client.delete(f"/songs/{song.song_id}", headers=headers)

    assert response.status_code == 200
    assert response.json() == {"message": "Song deleted successfully"}    

    # Check if the song is deleted
    db_song = db.query(Song).filter(Song.song_id == song.song_id).first()
    assert db_song is None

    # Clean up
    db.delete(artist)
    db.commit()

    # Check if the user is deleted
    db_artist = db.query(User).filter(User.id == artist.id).first()
    assert db_artist is None

def test_delete_no_ower_song():
    db = get_session()
    client = get_client()

    # Create an authenticated artist
    artist = create_random_auth_artist(db)
    headers = {"Authorization": f"Bearer {artist.token}"}
    song = create_random_song(db, artist.username)

    no_owner_artist = create_random_auth_artist(db)
    headers_no_owner = {"Authorization": f"Bearer {no_owner_artist.token}"}

    response = client.delete(f"/songs/{song.song_id}", headers=headers_no_owner)
    assert response.status_code == 403
    assert response.json() == {"detail": "You are not the owner of this song"}

    response = client.delete(f"/songs/{song.song_id}", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Song deleted successfully"}

    # Clean up
    db.delete(artist)
    db.delete(no_owner_artist)
    db.commit()

    # Check if the user is deleted
    db_artist = db.query(User).filter(User.id == artist.id).first()
    assert db_artist is None

    db_artist = db.query(User).filter(User.id == no_owner_artist.id).first()
    assert db_artist is None

def test_update_song_successful():
    db = get_session()
    client = get_client()

    # Create an authenticated artist
    artist = create_random_auth_artist(db)
    song = create_random_song(db, artist.username)
    headers = {"Authorization": f"Bearer {artist.token}"}
    song_data = {
        "title": random_lower_string(),
        "album": random_lower_string(),
        "genre": random_lower_string(),
        "release_date": "2024-11-26",
        "artist_name": artist.username
    }
    response = client.put(f"/songs/{song.song_id}", json=song_data, headers=headers)

    assert response.status_code == 200
    updated_song = response.json()
    assert updated_song["title"] == song_data["title"]
    assert updated_song["album"] == song_data["album"]
    assert updated_song["genre"] == song_data["genre"]
    assert updated_song["release_date"] == song_data["release_date"]
    assert updated_song["artist_name"] == artist.username

    # Check if the song is updated (refresh the song since this db is different from the one in the endpoint)
    db_song = db.query(Song).filter(Song.song_id == song.song_id).first()
    db.refresh(db_song)
    assert db_song.title == song_data["title"]
    assert db_song.album == song_data["album"]
    assert db_song.genre == song_data["genre"]
    assert db_song.release_date == song_data["release_date"]

    # Clean up
    db.delete(artist)
    db.delete(db_song)
    db.commit()

    # Check if the user is deleted
    db_artist = db.query(User).filter(User.id == artist.id).first()
    assert db_artist is None

    db_song = db.query(Song).filter(Song.song_id == song.song_id).first()
    assert db_song is None

def test_update_no_ower_song():
    db = get_session()
    client = get_client()

    # Create an authenticated artist
    artist = create_random_auth_artist(db)
    song = create_random_song(db, artist.username)
    song_data = {
        "title": random_lower_string(),
        "album": random_lower_string(),
        "genre": random_lower_string(),
        "release_date": "2024-11-26",
        "artist_name": artist.username
    }

    no_owner_artist = create_random_auth_artist(db)
    headers_no_owner = {"Authorization": f"Bearer {no_owner_artist.token}"}

    response = client.put(f"/songs/{song.song_id}", json=song_data, headers=headers_no_owner)
    assert response.status_code == 403
    assert response.json() == {"detail": "You are not the owner of this song"}

    # Get the song
    song = db.query(Song).filter(Song.song_id == song.song_id).first()


    # Clean up
    db.delete(artist)
    db.delete(no_owner_artist)
    db.delete(song)
    db.commit()

    # Check if the user is deleted
    db_artist = db.query(User).filter(User.id == artist.id).first()
    assert db_artist is None

    db_artist = db.query(User).filter(User.id == no_owner_artist.id).first()
    assert db_artist is None

    db_song = db.query(Song).filter(Song.song_id == song.song_id).first()
    assert db_song is None




    


