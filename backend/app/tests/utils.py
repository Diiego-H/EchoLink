import random
import string
from core.config import get_db
from main import app
from fastapi.testclient import TestClient
from models.user import UserInput, UserLogin, RoleEnum
from crud.user import authenticate, create_user
from crud.listener import get_listener_by_user_id
from crud.artist import get_artist_by_user_id
from models.song import SongInput
from crud.song import create_song

def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=10))

def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"

def create_random_user_input():
    username = random_lower_string()
    email = random_email()
    pwd = random_lower_string()
    return UserInput(username=username, email=email, password=pwd)

def create_random_listener_input():
    username = random_lower_string()
    email = random_email()
    pwd = random_lower_string()
    role = RoleEnum.listener
    return UserInput(username=username, email=email, password=pwd, role=role)

def create_random_artist_input():
    username = random_lower_string()
    email = random_email()
    pwd = random_lower_string()
    role = RoleEnum.artist
    return UserInput(username=username, email=email, password=pwd, role=role)

def create_random_user(db):
    return create_user(db, create_random_user_input())

def create_random_auth_user(db):
    user_input = create_random_user_input()
    user = create_user(db, user_input)
    authenticate(db, UserLogin(email=user_input.email, password=user_input.password))
    db.refresh(user)
    return user

def create_random_auth_listener(db):
    user_input = create_random_listener_input()
    user = create_user(db, user_input)
    authenticate(db, UserLogin(email=user_input.email, password=user_input.password))
    db.refresh(user)
    return user

def create_random_auth_artist(db):
    user_input = create_random_artist_input()
    user = create_user(db, user_input)
    authenticate(db, UserLogin(email=user_input.email, password=user_input.password))
    db.refresh(user)
    return user

def get_session():
    return next(get_db())

def get_client():
    return TestClient(app)

def create_artist(db, name="artist"):
    user_input = UserInput(email=f"{name}@{name}.com", username=name, password=name, role=RoleEnum.artist)
    user = create_user(db, user_input)
    return get_artist_by_user_id(db, user.id)

def create_listener(db, name="listener"):
    user_input = UserInput(email=f"{name}@{name}.com", username=name, password=name, role=RoleEnum.listener)
    user = create_user(db, user_input)
    return get_listener_by_user_id(db, user.id)

def create_random_artist(db):
    username = random_lower_string()
    password = random_lower_string()
    email = f"{username}@{username}.com"

    user_input = UserInput(username=username, email=email, password=password, role=RoleEnum.artist)
    user = create_user(db, user_input)

    return get_artist_by_user_id(db, user.id)

def create_random_listener(db):
    username = random_lower_string()
    password = random_lower_string()
    email = f"{username}@{username}.com"

    user_input = UserInput(username=username, email=email, password=password, role=RoleEnum.listener)
    user = create_user(db, user_input)

    return get_listener_by_user_id(db, user.id)

def create_random_song(db, artist_name, genre=None, title=None, release_date=None):
    song_data = {
        "title": title or random_lower_string(),
        "album": random_lower_string(),
        "genre": genre or random_lower_string(),
        "release_date": release_date or "2024-11-26",
        "artist_name": artist_name
    }
    return create_song(db, SongInput(**song_data))