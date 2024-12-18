from tests.utils import create_random_auth_user, get_session, get_client
from models.user import User
from core.security import create_access_token
from datetime import timedelta

def test_delete_account_successful():
    db = get_session()
    client = get_client()

    # Create an authenticated user
    user = create_random_auth_user(db)

    # Create a token for the user
    headers = {"Authorization": f"Bearer {user.token}"}

    # Delete the user account
    response = client.delete("/users/user", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"detail": "Account deleted successfully"}

    # check if the user is deleted
    assert db.query(User).filter(User.id == user.id).first() is None

def test_delete_account_user_not_found():
    client = get_client()

    # Create a token for a user that does not exist
    headers = {"Authorization": f"Bearer {create_access_token(999)}"}

    # Try to delete the account
    response = client.delete("/users/user", headers=headers)
    
    # Check if the response is correct
    assert response.status_code == 401
    assert response.json() == {"detail": "User not found"}

def test_delete_account_invalid_token_format():
    client = get_client()

    # Create a token with an invalid format
    headers = {"Authorization": "Bearer invalid_token"}

    # Try to delete the account
    response = client.delete("/users/user", headers=headers)

    # Check if the response is correct
    assert response.status_code == 403
    assert response.json() == {"detail": "Could not validate credentials"}

def test_delete_account_unauthorized():
    client = get_client()
    
    # Try to delete the account without authentication
    response = client.delete("/users/user")
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}
 

def test_delete_account_token_expired():
    client = get_client()

    # Create a token that has already expired (1 minute ago)
    expired_token = create_access_token(subject="testuser", expires_delta=timedelta(minutes=-1))

    # Create headers with the expired token
    headers = {"Authorization": f"Bearer {expired_token}"}

    # Try to delete the account with an expired token
    response = client.delete("/users/user", headers=headers)

    # Check if the response is correct
    assert response.status_code == 403
    assert response.json() == {"detail": "Token expired"}



   


