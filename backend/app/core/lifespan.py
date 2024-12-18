from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy.orm import Session
from core.config import SessionLocal
from crud.user import create_user, get_user_by_username
from crud.artist import get_artist_by_user_id
from crud.listener import follow_artist, get_listener_by_user_id, create_listener, check_follow
from crud.question import submit_question
from models.question import QuestionInput
from models.user import UserInput, RoleEnum, User
import json
from crud.artist import create_artist
from models.song import SongInput
from crud.song import create_song, get_songs_by_artist_id

# Define the lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    # populate_with_artists_and_songs()
    # populate_with_users()
    yield
    # Shutdown code (if needed)

# Add a test user to the database on startup
def init_db():
    db: Session = SessionLocal()
    try:
        user = get_user_by_username(db, "test")
        if not user:
            create_user(db, user.UserInput(username="test", email="test@test.com", password="test"))
    finally:
        db.close()



def populate_with_artists_and_songs():
    db: Session = SessionLocal()
    try:
        filename = 'data/top_artists.json'
        with open(filename, 'r', encoding='utf-8') as f:

            artists = json.load(f)  

        for artist in artists:

            user_input = UserInput(
                username=artist['name'].replace(' ', '_'),
                email=artist['email'],
                password=artist['password'],
                role=RoleEnum.artist,
                image_url=artist['image_url'],
                genre=artist['genres'],
                description=artist['description']
            )

            songs_list = artist['songs']
            existing_user_by_username = db.query(User).filter(User.username == user_input.username).first()

            if not existing_user_by_username:
                user = create_user(db, user_input)
            else:
                user = get_user_by_username(db, user_input.username)

            artist = get_artist_by_user_id(db, user.id)

            if not artist:
                artist = create_artist(db, user)

            artist_song_list = get_songs_by_artist_id(db, artist.artist_id)
            artist_song_list = [song.title for song in artist_song_list]	
            song_counter = 0
            for song in songs_list:
                song_counter += 1
                # Add songs to the artist's profile
                song_input = SongInput(
                    title=song['name'],
                    release_date=song['release_date'],
                    album=song['album'],
                    genre=song['genre'],
                    artist_name=artist.name,
                    sources=song['sources']
                )
                if song_counter == 5:
                    break

                if song_input.title not in artist_song_list:
                    song = create_song(db, song_input)

    except Exception as e:
        print(e)
    finally:
        db.close()



def populate_with_users():
    db: Session = SessionLocal()
    try:
        filename = 'data/user.json'
        with open(filename, 'r', encoding='utf-8') as f:
            users = json.load(f)
        
        for user in users.values():

            user_input = UserInput(
                username=user['username'],
                email=user['email'],
                password=user['password'],
                role=RoleEnum.listener
            )

            question_list = user["artist_questions"]
            followed_artists = user["followers"]

            existing_user_by_username = db.query(User).filter(User.username == user_input.username).first()

            if not existing_user_by_username:
                user = create_user(db, user_input)
            else:
                user = get_user_by_username(db, user_input.username)

            listener = get_listener_by_user_id(db, user.id)

            if not listener:
                listener = create_listener(db, user)

            for artist in followed_artists:
                follow = check_follow(db, listener, artist)
                if not follow:
                    follow_artist(db, listener, artist)

            for artist, question in question_list.items():
                question = QuestionInput(
                    artist_username=artist,
                    question_text=question
                )
                try:    
                    submit_question(db, listener, question)
                except Exception as e:
                    print(e)
                    

    except Exception as e:
        print(e)
    finally:
        db.close()