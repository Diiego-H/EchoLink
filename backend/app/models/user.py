""" Models """
from typing import Optional
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.config import Base
from pydantic import BaseModel, field_validator, HttpUrl
import re
import enum

# Follow relationship between listeners and artists
class ListenerArtistLink(Base):
    __tablename__ = "listener_artist_link"

    listener_id = Column(Integer, ForeignKey('listeners.listener_id', ondelete="CASCADE"), primary_key=True)
    artist_id = Column(Integer, ForeignKey('artists.artist_id', ondelete="CASCADE"), primary_key=True)
    follow_date = Column(DateTime, default=func.now(), nullable=False)

# Enum for profile visibility
class VisibilityEnum(enum.Enum):
    public = "public"
    private = "private"

# Enum for user roles
class RoleEnum(enum.Enum):
    listener = "listener"
    artist = "artist"

# User table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, index=True, primary_key=True)
    username = Column(String, index=True, unique=True)
    email = Column(String, index=True, unique=True)
    hashed_password = Column(String)
    token = Column(String, default=None)
    description = Column(String, nullable=True)
    genre = Column(String, nullable=True)
    visibility = Column(Enum(VisibilityEnum), default=VisibilityEnum.public)
    role = Column(Enum(RoleEnum), default=None, nullable=True)
    image_url = Column(String, default=None, nullable=True)

    # Relationship with Playlist
    playlists = relationship("Playlist", back_populates="user", cascade="all, delete-orphan")

# Validation mixin class
class UserValidationMixin(BaseModel):
    # Validator for email field
    @field_validator('email', check_fields=False)
    def validate_email(cls, v):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise ValueError('Incorrect email format.')
        return v

    # Validator for password field
    @field_validator('password', check_fields=False)
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long.')
        return v

    # Validator for username field
    @field_validator('username', check_fields=False)
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z_0-9]{4,16}$', v):
            raise ValueError('Username must be 4-16 characters long, containing only letters, numbers, and underscores.')
        return v
    
    # Validator for image URL
    @field_validator('image_url', check_fields=False)
    def validate_image_url(cls, v):
        return v

# Input user for login
class UserLogin(UserValidationMixin):
    email: str
    password: str

# JSON payload containing access token
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str = None

# Contents of JWT token
class TokenPayload(BaseModel):
    sub: int = None

# Input user for register
class UserInput(UserLogin):
    username: str
    description: Optional[str] = None
    genre: Optional[str] = None
    visibility: Optional[VisibilityEnum] = VisibilityEnum.public
    role: Optional[RoleEnum] = RoleEnum.listener
    image_url: Optional[HttpUrl] = None
    description: Optional[str] = None

# Output user
class UserOutput(BaseModel):
    username: str
    email: str
    description: Optional[str] = None
    genre: Optional[str] = None
    visibility: VisibilityEnum
    role: RoleEnum
    image_url: Optional[HttpUrl] = None

    # Pydantic V2 configuration for ORM mode
    model_config = {'from_attributes': True}

# Update user
class UserUpdate(UserValidationMixin):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    description: Optional[str] = None
    genre: Optional[str] = None
    visibility: Optional[VisibilityEnum] = None
