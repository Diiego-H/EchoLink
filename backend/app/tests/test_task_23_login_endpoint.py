from core.config import get_db
from tests.utils import create_random_user, create_random_user_input
from models.user import UserLogin
from crud.user import create_user, authenticate
import pytest
from fastapi.testclient import TestClient
from main import app

def test_invalid_fields():
    # Invalid email format
    with pytest.raises(ValueError, match="Incorrect email format."):
        UserLogin(email="hello", password="world")

    # Password too short
    with pytest.raises(ValueError, match="Password must be at least 6 characters long."):
        UserLogin(email="hello@hello.com", password="world")    

def test_failed_authentication():
    db = next(get_db())

    # Inexistent account for an email
    with pytest.raises(ValueError, match="The email is not associated to any account."):
        authenticate(db, UserLogin(email="not@found.email", password="whatever"))

    # Random user
    user = create_random_user(db)

    # Incorrect password for this user
    with pytest.raises(ValueError, match="Incorrect password."):
        authenticate(db, UserLogin(email=user.email, password="whatever"))

    # Delete data created
    db.delete(user)
    db.commit()

def test_successful_authentication():
    db = next(get_db())

    # Random user
    user_input = create_random_user_input()
    user = create_user(db, user_input)

    # Get JWT
    user = authenticate(db, UserLogin(email=user_input.email, password=user_input.password))
    token = user.token

    # Check token is valid
    assert token is not None
    assert type(token) is str

    # Deleta data created
    db.delete(user)
    db.commit()


def test_failed_login():
    db = next(get_db())
    client = TestClient(app)

    # Inexistent account for an email
    response = client.post("/login", json={"email": "not@found.email", "password": "whatever"})
    assert response.status_code == 400
    assert response.json()["detail"] == "The email is not associated to any account."

    # Random user
    user = create_random_user(db)

    # Incorrect password for this user
    response = client.post("/login", json={"email": user.email, "password": "whatever"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect password."

    # Delete data created
    db.delete(user)
    db.commit()


def test_successful_login():
    db = next(get_db())
    client = TestClient(app)

    # Random user
    user_input = create_random_user_input()
    user = create_user(db, user_input)

    # Successful login
    response = client.post("/login", json={"email": user_input.email, "password": user_input.password})

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["access_token"] is not None
    assert type(response.json()["access_token"]) is str
    assert response.json()["token_type"] == "bearer"
    assert "username" in response.json()

    # Delete data created
    db.delete(user)
    db.commit()
