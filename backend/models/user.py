from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = 'users'

    id                  = Column(Integer, primary_key=True, index=True)
    name                = Column(String(255), nullable=False)
    email               = Column(String(255), unique=True, index=True, nullable=False)
    password            = Column(String(255), nullable=False)
    created_at          = Column(DateTime, default=datetime.utcnow)

    # New columns for password reset
    reset_token         = Column(String(255), nullable=True)
    reset_token_expiry  = Column(DateTime, nullable=True)

    conversations = relationship('Conversation', back_populates='user')
    