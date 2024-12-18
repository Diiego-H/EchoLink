"""Models"""
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Enum, Boolean, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.config import Base
import enum
from pydantic import BaseModel, ConfigDict

# Enum for response status
class ResponseEnum(enum.Enum):
    waiting = "waiting"
    answered = "answered"
    rejected = "rejected"

# Questions table
class Question(Base):
    __tablename__ = "questions"

    question_id = Column(Integer, primary_key=True, index=True)
    listener_id = Column(Integer, ForeignKey('listeners.listener_id', ondelete="CASCADE"), nullable=False)
    artist_id = Column(Integer, ForeignKey('artists.artist_id', ondelete="CASCADE"), nullable=False)
    artist_username = Column(String, nullable=True)
    listener_username = Column(String, nullable=True)
    question_text = Column(Text, nullable=False)
    response_text = Column(Text, nullable=True)
    question_date = Column(DateTime, default=func.now(), nullable=False)
    response_date = Column(DateTime, nullable=True)
    response_status = Column(Enum(ResponseEnum), default=ResponseEnum.waiting)
    archived = Column(Boolean, default=False, nullable=False)

    # Relationships to other tables
    listener = relationship("Listener")
    artist = relationship("Artist")

# Input data for question submission
class QuestionInput(BaseModel):
    artist_username: str
    question_text: str

# Input data for question response
class QuestionResponse(BaseModel):
    question_id: int
    response_text: str

# Pydantic model to return Question data
class QuestionModel(BaseModel):
    question_id: int
    listener_id: int
    artist_username: Optional[str]
    listener_username: Optional[str]
    artist_id: int
    question_text: str
    response_text: Optional[str]
    question_date: datetime
    response_date: Optional[datetime]
    response_status: ResponseEnum
    archived: bool

    # Use ConfigDict for Pydantic v2
    model_config = ConfigDict(from_attributes=True)