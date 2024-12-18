""" Models """
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from core.config import Base

# Listener table
class Listener(Base):
    __tablename__ = "listeners"

    listener_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), unique=True, nullable=False)

    # Relationship to the User table
    user = relationship("User")
