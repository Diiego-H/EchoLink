from core.config import get_db
from tests.utils import random_lower_string, random_email, create_random_auth_user
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_update_user_success():
    # Create a random user and save it to the database
    db = next(get_db())
    user = create_random_auth_user(db)

    # Prepare the data to update the user
    new_email = random_email()
    new_username = random_lower_string()

    # Set headers with the Authorization token
    headers = {"Authorization": f"Bearer {user.token}"}

    # Make the PUT request to update the user
    response = client.put("/users/user", json={
        "username": new_username,
        "email": new_email,
        "password": "newpassword",
        "description": "Updated description",
        "genre": "Updated genre",
        "visibility": "private"
    }, headers=headers)

    # Check the response is successful
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user['username'] == new_username
    assert updated_user['email'] == new_email
    assert updated_user['description'] == "Updated description"
    assert updated_user['genre'] == "Updated genre"
    assert updated_user['visibility'] == "private"

    # Clean up by deleting the test user from the database
    db.delete(user)
    db.commit()

def test_update_user_username_taken():
    db = next(get_db())
    user1 = create_random_auth_user(db)
    user2 = create_random_auth_user(db)

    # Set headers with the Authorization token
    headers = {"Authorization": f"Bearer {user1.token}"}

    # Attempt to update user1's username to user2's username, which is already taken
    response = client.put("/users/user", json={
        "username": user2.username,
        "email": "new_email@example.com",
        "password": "newpassword"
    }, headers=headers)

    # Check that the response returns a conflict error
    assert response.status_code == 400
    assert response.json()['detail'] == "Username already exists."

    # Clean up by deleting the test users
    db.delete(user1)
    db.delete(user2)
    db.commit()

def test_update_user_email_taken():
    db = next(get_db())
    user1 = create_random_auth_user(db)
    user2 = create_random_auth_user(db)

    # Set headers with the Authorization token
    headers = {"Authorization": f"Bearer {user1.token}"}

    # Attempt to update user1's email to user2's email, which is already taken
    response = client.put("/users/user", json={
        "username": "new_username",
        "email": user2.email,
        "password": "newpassword"
    }, headers=headers)

    # Check that the response returns a conflict error
    assert response.status_code == 400
    assert response.json()['detail'] == "Email already exists."

    # Clean up by deleting the test users
    db.delete(user1)
    db.delete(user2)
    db.commit()

def test_update_user_invalid_email():
    db = next(get_db())
    user = create_random_auth_user(db)

    # Set headers with the Authorization token
    headers = {"Authorization": f"Bearer {user.token}"}

    # Attempt to update the user's email to an invalid format
    response = client.put("/users/user", json={
        "username": "new_username",
        "email": "invalid_email",
        "password": "newpassword"
    }, headers=headers)

    # Check that the response returns a validation error
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "Value error, Incorrect email format."

    # Clean up by deleting the test user
    db.delete(user)
    db.commit()

def test_update_user_invalid_username():
    db = next(get_db())
    user = create_random_auth_user(db)

    # Set headers with the Authorization token
    headers = {"Authorization": f"Bearer {user.token}"}

    # Attempt to update the username to an invalid format (too short)
    response = client.put("/users/user", json={
        "username": "inv",
        "email": "new_email@example.com",
        "password": "newpassword"
    }, headers=headers)

    # Check that the response returns a validation error
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "Value error, Username must be 4-16 characters long, containing only letters, numbers, and underscores."

    # Clean up by deleting the test user
    db.delete(user)
    db.commit()

def test_update_user_invalid_password():
    db = next(get_db())
    user = create_random_auth_user(db)

    # Set headers with the Authorization token
    headers = {"Authorization": f"Bearer {user.token}"}

    # Attempt to update the user's password to an invalid value (too short)
    response = client.put("/users/user", json={
        "username": "new_username",
        "email": "new_email@example.com",
        "password": "short"
    }, headers=headers)

    # Check that the response returns a validation error
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "Value error, Password must be at least 6 characters long."

    # Clean up by deleting the test user
    db.delete(user)
    db.commit()

def test_update_user_partial_data():
    db = next(get_db())
    user = create_random_auth_user(db)

    # Set headers with the Authorization token
    headers = {"Authorization": f"Bearer {user.token}"}

    # Attempt to update the user with only some of the fields (e.g., only update email)
    new_email = random_email()
    response = client.put("/users/user", json={
        "email": new_email
    }, headers=headers)

    # Check the response is successful and the email is updated
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user['email'] == new_email

    # Clean up by deleting the test user
    db.delete(user)
    db.commit()
