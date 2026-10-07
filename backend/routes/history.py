from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from database import get_db
from models.conversation import Conversation
from routes.auth import decode_token

router = APIRouter()

def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith('Bearer '):
        raise HTTPException(status_code=401, detail='Invalid token format')
    return decode_token(authorization.split(' ')[1])

class SaveRequest(BaseModel):
    conversation_id: Optional[int] = None
    title: str
    topic: Optional[str] = None
    messages: list

@router.get('/')
def get_conversations(user=Depends(get_current_user), db: Session=Depends(get_db)):
    convos = db.query(Conversation).filter(
        Conversation.user_id == int(user['sub'])
    ).order_by(Conversation.updated_at.desc()).all()
    return [{'id': c.id, 'title': c.title, 'topic': c.topic, 'updated_at': c.updated_at.isoformat()} for c in convos]

@router.get('/{conversation_id}')
def get_conversation(conversation_id: int, user=Depends(get_current_user), db: Session=Depends(get_db)):
    c = db.query(Conversation).filter(Conversation.id==conversation_id, Conversation.user_id==int(user['sub'])).first()
    if not c: raise HTTPException(status_code=404, detail='Not found')
    return {'id': c.id, 'title': c.title, 'topic': c.topic, 'messages': c.get_messages()}

@router.post('/save')
def save_conversation(data: SaveRequest, user=Depends(get_current_user), db: Session=Depends(get_db)):
    uid = int(user['sub'])
    if data.conversation_id:
        c = db.query(Conversation).filter(Conversation.id==data.conversation_id, Conversation.user_id==uid).first()
        if not c: raise HTTPException(status_code=404, detail='Not found')
    else:
        c = Conversation(user_id=uid)
        db.add(c)
    c.title = data.title
    c.topic = data.topic
    c.set_messages(data.messages)
    db.commit(); db.refresh(c)
    return {'id': c.id, 'title': c.title}

@router.delete('/{conversation_id}')
def delete_conversation(conversation_id: int, user=Depends(get_current_user), db: Session=Depends(get_db)):
    c = db.query(Conversation).filter(Conversation.id==conversation_id, Conversation.user_id==int(user['sub'])).first()
    if not c: raise HTTPException(status_code=404, detail='Not found')
    db.delete(c); db.commit()
    return {'message': 'Deleted'}