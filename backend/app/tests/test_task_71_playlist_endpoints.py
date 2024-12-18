from fastapi.testclient import TestClient
from crud.playlist import create_playlist, get_playlist_by_id
from main import app
from core.config import get_db
from models.playlist import PlaylistInput, VisibilityEnum
from tests.utils import create_random_auth_user

client = TestClient(app)

# Test for creating a playlist
def test_create_playlist():
    db = next(get_db())

    # Create a random user
    user = create_random_auth_user(db)

    playlist_json = {
        "name": "Test Playlist",
        "description": "Test description",
        "visibility": "public"
    }

    # Send POST request to create the playlist
    response = client.post(
        "/playlist",
        json=playlist_json,
        headers={"Authorization": f"Bearer {user.token}"}
    )

    # Assert response status and content
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Playlist"
    assert data["description"] == "Test description"
    assert data["visibility"] == "public"
    assert data["username"] == user.username  # Assert that the playlist is associated with the user

    # Cleanup: Delete the user and playlist
    db.delete(user)
    db.commit()

# Test for retrieving a playlist by ID
def test_get_playlist_by_id():
    db = next(get_db())

    # Create a random user
    user = create_random_auth_user(db)

    # Create a playlist for that user
    playlist_data = PlaylistInput(
        name="Retrieve Playlist",
        description="Test retrieve",
        visibility=str(VisibilityEnum.public.value)
    )
    playlist = create_playlist(db, playlist_data, user.id)

    # Send GET request to retrieve the playlist
    response = client.get(
        f"/playlist/{playlist.playlist_id}"
    )

    # Assert response status and content
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Retrieve Playlist"
    assert data["description"] == "Test retrieve"

    # Cleanup: Delete the user and playlist
    db.delete(user)
    db.commit()

# Test for updating a playlist
def test_update_playlist():
    db = next(get_db())

    # Create a random user
    user = create_random_auth_user(db)

    # Create a playlist for that user
    playlist_data = PlaylistInput(
        name="Old Playlist",
        description="Old description",
        visibility=str(VisibilityEnum.public.value)
    )
    playlist = create_playlist(db, playlist_data, user.id)

    # Define update data
    update_json = {
        "name": "Updated Playlist",
        "description": "Updated description"
    }

    # Send PUT request to update the playlist
    response = client.put(
        f"/playlist/{playlist.playlist_id}",
        json=update_json,
        headers={"Authorization": f"Bearer {user.token}"}
    )

    # Assert response status and content
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Playlist"
    assert data["description"] == "Updated description"

    # Cleanup: Delete the user and playlist
    db.delete(user)
    db.commit()

# Test for deleting a playlist
def test_delete_playlist():
    db = next(get_db())

    # Create a random user
    user = create_random_auth_user(db)

    # Create a playlist for that user
    playlist_data = PlaylistInput(
        name="Delete Playlist",
        description="Test delete",
        visibility=str(VisibilityEnum.public.value)
    )
    playlist = create_playlist(db, playlist_data, user.id)

    # Send DELETE request to delete the playlist
    response = client.delete(
        f"/playlist/{playlist.playlist_id}",
        headers={"Authorization": f"Bearer {user.token}"}
    )

    # Assert response status
    assert response.status_code == 204

    # Ensure the playlist was deleted from the database
    try:
        get_playlist_by_id(db, playlist.playlist_id, user.id)
        assert False  # The playlist should not exist
    except ValueError:
        pass # Expected

    # Cleanup: Delete the user
    db.delete(user)
    db.commit()

# Test for retrieving playlists by username
def test_get_playlists_by_username():
    db = next(get_db())

    # Create a random user
    user = create_random_auth_user(db)

    # Create a playlist for that user
    playlist_data = PlaylistInput(
        name="User Playlist",
        description="Test user playlists",
        visibility=str(VisibilityEnum.public.value)
    )
    create_playlist(db, playlist_data, user.id)

    # Send GET request to retrieve playlists by username
    response = client.get(
        f"playlist/user/{user.username}"
    )

    # Assert response status and content
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == "User Playlist"

    # Cleanup: Delete the user and playlist
    db.delete(user)
    db.commit()
