from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.lifespan import lifespan
from core.config import engine
from core.config import Base
from routes import user, test, login, question, listener, artist, song, playlist, metrics
# Importing them ensures SQLAlchemy creates their tables.
from models.user import User, ListenerArtistLink  # noqa: F401
from models.artist import Artist  # noqa: F401
from models.listener import Listener # noqa: F401
from models.question import Question # noqa: F401
from models.song import Song, SongSource # noqa: F401
from models.playlist import Playlist # noqa: F401


# Initialize the FastAPI app with the lifespan context manager
app = FastAPI(lifespan=lifespan)


# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, change this to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Create the database tables on startup
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(test.router, prefix="/test", tags=["Test"])
app.include_router(login.router, prefix="/login", tags=["Login"])
app.include_router(question.router, prefix="/questions", tags=["Questions"])
app.include_router(listener.router, prefix="/listeners", tags=["Listeners"])
app.include_router(artist.router, prefix="/artists", tags=["Artists"])
app.include_router(song.router, prefix="/songs", tags=["Songs"])
app.include_router(playlist.router, prefix="/playlist", tags=["Playlist"])
app.include_router(metrics.router, prefix="/metrics", tags=["Metrics"])
