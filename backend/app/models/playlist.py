""" Models """
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Enum
from sqlalchemy.orm import relationship
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from core.config import Base
import enum

# Enum for playlist visibility
class VisibilityEnum(enum.Enum):
    public = "public"
    private = "private"

# Association table for playlist and songs
playlist_songs = Table(
    'playlist_songs',
    Base.metadata,
    Column('playlist_id', Integer, ForeignKey('playlists.playlist_id', ondelete="CASCADE"), primary_key=True),
    Column('song_id', Integer, ForeignKey('songs.song_id', ondelete="CASCADE"), primary_key=True),
    Column('order', Integer, nullable=False)
)

# Playlist table
class Playlist(Base):
    __tablename__ = "playlists"

    playlist_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    visibility = Column(Enum(VisibilityEnum), default=VisibilityEnum.public)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)

    # Relationship with User
    user = relationship("User", back_populates="playlists")

    # Relationship with Song
    songs = relationship("Song", secondary=playlist_songs, back_populates="playlists", order_by=playlist_songs.c.order)

# Pydantic model for playlist input
class PlaylistInput(BaseModel):
    name: str
    description: Optional[str] = None
    visibility: VisibilityEnum = VisibilityEnum.public

    # Use ConfigDict for Pydantic v2
    model_config = ConfigDict(from_attributes=True)

# Pydantic model for song output
class SongOutput(BaseModel):
    song_id: int

    # Use ConfigDict for Pydantic v2
    model_config = ConfigDict(from_attributes=True)

# Pydantic model for playlist output
class PlaylistOutput(BaseModel):
    playlist_id: int
    name: str
    description: Optional[str] = None
    visibility: VisibilityEnum
    username: str
    songs: List[SongOutput]

    # Use ConfigDict for Pydantic v2
    model_config = ConfigDict(from_attributes=True)

# Pydantic model for playlist update
class PlaylistUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    visibility: Optional[VisibilityEnum] = None

    # Use ConfigDict for Pydantic v2
    model_config = ConfigDict(from_attributes=True)
