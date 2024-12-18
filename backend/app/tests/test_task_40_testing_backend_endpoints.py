from models.user import UserLogin
from models.user import User
from tests.utils import create_random_user_input, get_session, get_client, create_random_auth_user, random_email, random_lower_string
from crud.user import authenticate


def test_1_simulation():
    """
    In this test, we will create a user with a specific email address. After that, we will delete 
    the initial user.
    """

    # Get the database and client
    db = get_session()
    client = get_client()

    # Create an authenticated user
    user_input = create_random_user_input()
    response = client.post("/users/user", json={"username": user_input.username, "email": user_input.email, "password": user_input.password})

    # Check object returned
    assert response.status_code == 200
    assert response.json()['username'] == user_input.username

    # Get the user from the database
    user = db.query(User).filter(User.email == user_input.email).first()

    # Check no token in database
    assert user.token is None

    # Create a token for the user
    user = authenticate(db, UserLogin(email=user_input.email, password=user_input.password))

    # Check token in database
    headers = {"Authorization": f"Bearer {user.token}"}
    assert user.token is not None

    # Delete the user account
    response = client.delete("/users/user", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"detail": "Account deleted successfully"}

    # Check if the user is deleted
    assert db.query(User).filter(User.id == user.id).first() is None


def test_2_simulation():
    """
    In this test, we will first create a user with a specific email address. Next, we will attempt to 
    create a second user using the same email. This operation should fail because the email is already 
    taken. After that, we will delete the initial user. Finally, we will attempt to create a new user 
    with the same email and confirm that this time, the creation is successful.
    """

    # Get the database and client
    db = get_session()
    client = get_client()

    # Create an authenticated user
    user_input = create_random_user_input()
    response = client.post("/users/user", json={"username": user_input.username, "email": user_input.email, "password": user_input.password})

    # Check object returned
    assert response.status_code == 200
    assert response.json()['username'] == user_input.username

    # Get the user from the database
    user = db.query(User).filter(User.email == user_input.email).first()

    # Check no token in database
    assert user.token is None

    # Create a token for the user
    user = authenticate(db, UserLogin(email=user_input.email, password=user_input.password))

    # Check token in database
    headers = {"Authorization": f"Bearer {user.token}"}
    assert user.token is not None

    # Create another user with the same email
    response = client.post("/users/user", json={"username": "new_username", "email": user_input.email, "password": "123456"})
    assert response.status_code == 400
    assert response.json()['detail'] == "Email already exists."

    # Delete the user account
    response = client.delete("/users/user", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"detail": "Account deleted successfully"}

    # Create another user with the same email
    response = client.post("/users/user", json={"username": "new_username", "email": user_input.email, "password": "123456" })

    # Check object returned
    assert response.status_code == 200
    assert response.json()['username'] == "new_username"

    # Get the user from the database
    user2 = db.query(User).filter(User.email == user_input.email).first()

    # Check no token in database
    assert user2.token is None

    # Create a token for the user
    user2 = authenticate(db, UserLogin(email=user_input.email, password="123456"))

    # Check token in database
    headers = {"Authorization": f"Bearer {user2.token}"}
    assert user2.token is not None

    # Delete the user account
    response = client.delete("/users/user", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"detail": "Account deleted successfully"}

    # Check if the user is deleted
    assert db.query(User).filter(User.id == user2.id).first() is None


def test_3_simulation():
    """"
    In this test, we will create an specific user. Then we will attempt to update the username
    of the user. After that, we will try to check if the token is the same. Finally, we will
    delete the user.
    """

    # Get the database and client
    db = get_session()
    client = get_client()

    # Create an authenticated user
    user_input = create_random_auth_user(db)
    new_email = random_email()
    new_username = random_lower_string()

    # Set headers with the Authorization token
    headers = {"Authorization": f"Bearer {user_input.token}"}

    # Attempt to update user's username
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

    # Get the user from the database
    response = client.get(f"/users/{new_username}")    

    # Check that the response is successful and returns the correct data
    assert response.status_code == 200
    assert response.json()['username'] == new_username

    user = db.query(User).filter(User.username == new_username).first()
    
    # Check token
    assert user.token == user_input.token

    # Delete the user account
    response = client.delete("/users/user", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"detail": "Account deleted successfully"}

    # Check if the user is deleted
    assert db.query(User).filter(User.id == user.id).first() is None

def test_4_simulation():
    """"
    In this test, we will create an specific user. Then we will attempt to logout the user. 
    Due to the logout, the token will be deleted. Finally, we will delete the user.
    """

    # Get the database and client
    db = get_session()
    client = get_client()

    # Create an authenticated user
    user_input = create_random_user_input()
    response = client.post("/users/user", json={"username": user_input.username, "email": user_input.email, "password": user_input.password})

    # Check object returned
    assert response.status_code == 200
    assert response.json()['username'] == user_input.username

    # Get the user from the database
    user = db.query(User).filter(User.email == user_input.email).first()

    # Check no token in database
    assert user.token is None

    # Create a token for the user
    user = authenticate(db, UserLogin(email=user_input.email, password=user_input.password))

    # Check token in database
    headers = {"Authorization": f"Bearer {user.token}"}
    assert user.token is not None

    # Logout the user
    response = client.post("login/logout", headers=headers)
    assert response.status_code == 200

    # Check token is None
    db.refresh(user)
    assert user.token is None

    # Delete the user account
    db.delete(user)
    db.commit()

    # Check if the user is deleted
    assert db.query(User).filter(User.id == user.id).first() is None









