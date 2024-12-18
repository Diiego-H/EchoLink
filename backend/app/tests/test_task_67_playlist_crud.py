from sqlalchemy.orm import Session
from core.config import get_db
from crud.playlist import create_playlist, get_playlist_by_id, update_playlist, delete_playlist
from models.playlist import PlaylistInput, PlaylistUpdate, Playlist
from tests.utils import create_random_user

# Test for creating a playlist
def test_create_playlist():
    db: Session = next(get_db())

    # Create a random user
    user = create_random_user(db)

    # Define input for the playlist
    playlist_input = PlaylistInput(
        name="Test Playlist",
        description="A playlist for testing purposes",
        visibility="public",
    )

    # Create the playlist
    playlist = create_playlist(db, playlist_input, user.id)

    # Check that the playlist was created successfully
    assert playlist is not None
    assert playlist.name == "Test Playlist"
    assert playlist.description == "A playlist for testing purposes"
    assert playlist.visibility.value == "public"
    assert playlist.user_id == user.id

    # Cleanup
    db.delete(playlist)
    db.delete(user)
    db.commit()

# Test for retrieving a playlist by ID
def test_get_playlist_by_id():
    db: Session = next(get_db())

    # Create a random user
    user = create_random_user(db)

    # Create a playlist
    playlist = Playlist(
        name="Retrieve Playlist",
        description="Retrieve test description",
        visibility="private",
        user_id=user.id
    )
    db.add(playlist)
    db.commit()
    db.refresh(playlist)

    # Retrieve the playlist by ID
    retrieved_playlist = get_playlist_by_id(db, playlist.playlist_id, user.id)

    # Validate the retrieved playlist
    assert retrieved_playlist is not None
    assert retrieved_playlist.playlist_id == playlist.playlist_id
    assert retrieved_playlist.name == "Retrieve Playlist"

    # Cleanup
    db.delete(playlist)
    db.delete(user)
    db.commit()

# Test for updating a playlist
def test_update_playlist():
    db: Session = next(get_db())

    # Create a random user
    user = create_random_user(db)

    # Create a playlist
    playlist = Playlist(
        name="Old Playlist Name",
        description="Old Description",
        visibility="public",
        user_id=user.id
    )
    db.add(playlist)
    db.commit()
    db.refresh(playlist)

    # Define the update data
    playlist_update = PlaylistUpdate(
        name="Updated Playlist Name",
        description="Updated Description"
    )

    # Update the playlist
    updated_playlist = update_playlist(db, playlist.playlist_id, playlist_update, user.id)

    # Validate the updated playlist
    assert updated_playlist is not None
    assert updated_playlist.name == "Updated Playlist Name"
    assert updated_playlist.description == "Updated Description"

    # Cleanup
    db.delete(playlist)
    db.delete(user)
    db.commit()

# Test for updating a playlist partially
def test_partial_update_playlist():
    db: Session = next(get_db())

    # Create a random user
    user = create_random_user(db)

    # Create a playlist
    playlist = Playlist(
        name="Old Playlist Name",
        description="Old Description",
        visibility="public",
        user_id=user.id
    )
    db.add(playlist)
    db.commit()
    db.refresh(playlist)

    # Define the update data
    playlist_update = PlaylistUpdate(
        name="Updated Playlist Name"
    )

    # Update the playlist
    updated_playlist = update_playlist(db, playlist.playlist_id, playlist_update, user.id)

    # Validate the updated playlist
    assert updated_playlist is not None
    assert updated_playlist.name == "Updated Playlist Name"
    assert updated_playlist.description == "Old Description"

    # Cleanup
    db.delete(playlist)
    db.delete(user)
    db.commit()

# Test for updating a playlist with permission error
def test_update_playlist_permission_error():
    db: Session = next(get_db())

    # Create a random user
    user1 = create_random_user(db)
    user2 = create_random_user(db)  # This user will try to update someone else's playlist

    # Create a playlist for user1
    playlist = Playlist(
        name="Test Playlist",
        description="Test Description",
        visibility="public",
        user_id=user1.id
    )
    db.add(playlist)
    db.commit()
    db.refresh(playlist)

    # Attempt to update playlist with user2 (should raise ValueError)
    playlist_update = PlaylistUpdate(
        name="New Name"
    )
    try:
        update_playlist(db, playlist.playlist_id, playlist_update, user2.id)
        assert False, "Expected ValueError but did not raise"
    except ValueError:
        pass  # Expected result

    # Cleanup
    db.delete(playlist)
    db.delete(user1)
    db.delete(user2)
    db.commit()

# Test for deleting a playlist
def test_delete_playlist():
    db: Session = next(get_db())

    # Create a random user
    user = create_random_user(db)

    # Create a playlist
    playlist = Playlist(
        name="Delete Playlist",
        description="This playlist will be deleted",
        visibility="public",
        user_id=user.id
    )
    db.add(playlist)
    db.commit()
    db.refresh(playlist)

    # Delete the playlist
    delete_playlist(db, playlist.playlist_id, user.id)

    # Verify the playlist was deleted
    deleted_playlist = db.query(Playlist).filter(Playlist.playlist_id == playlist.playlist_id).first()
    assert deleted_playlist is None

    # Cleanup
    db.delete(user)
    db.commit()
