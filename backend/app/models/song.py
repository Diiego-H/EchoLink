""" Models """
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.config import Base
from pydantic import BaseModel, ConfigDict, HttpUrl
from typing import Optional, List

# Song table
class Song(Base):
    __tablename__ = "songs"

    song_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    album = Column(String, nullable=True)
    genre = Column(String, nullable=True)
    release_date = Column(String, nullable=False)
    artist_id = Column(Integer, ForeignKey('artists.artist_id', ondelete="CASCADE"), nullable=False)

    # Relationship with Artist
    artist = relationship("Artist", back_populates="songs")

    # Relationship with Playlist
    playlists = relationship("Playlist", secondary="playlist_songs", back_populates="songs")

    # Relationship with SongSource
    sources = relationship("SongSource", back_populates="song", 
                           cascade="all, delete-orphan",  # Ensures proper cascading behavior
                           passive_deletes=True  # Lets the database handle deletions
    )

    @property
    def source_urls(self):
        """Return a list of source URLs."""
        return [source.source_url for source in self.sources]


# SongSource table
class SongSource(Base):
    __tablename__ = "song_sources"

    id = Column(Integer, primary_key=True, index=True)
    song_id = Column(Integer, ForeignKey('songs.song_id', ondelete="CASCADE"), nullable=False)
    source_url = Column(String, nullable=False)

    # Relationship with Song
    song = relationship("Song", back_populates="sources")


# Pydantic model for song input
class SongInput(BaseModel):
    title: str
    release_date: str
    album: Optional[str] = None
    genre: Optional[str] = None
    artist_name: str
    sources: Optional[List[HttpUrl]] = [] # List of source URLs

    # Use ConfigDict for Pydantic v2
    model_config = ConfigDict(from_attributes=True)


# Pydantic model for song output
class SongOutput(BaseModel):
    song_id: int
    title: str
    album: Optional[str] = None
    genre: Optional[str] = None
    release_date: str
    artist_name: str
    sources: List[str]  # List of source URLs

    # Use ConfigDict for Pydantic v2
    model_config = ConfigDict(from_attributes=True)
