from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import json
from database import Base

class Conversation(Base):
    __tablename__ = 'conversations'

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey('users.id'), nullable=False)
    title      = Column(String(255), default='New conversation')  # ← added length
    topic      = Column(String(100), nullable=True)               # ← added length
    messages   = Column(Text, default='[]')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship('User', back_populates='conversations')

    def get_messages(self):
        return json.loads(self.messages)

    def set_messages(self, messages_list):
        self.messages = json.dumps(messages_list)