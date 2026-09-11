import uuid
from app.database import SessionLocal
from app.models.conversation import Conversation


def create_conversation(title: str = "New conversation") -> dict:
    db = SessionLocal()
    try:
        conversation = Conversation(thread_id=str(uuid.uuid4()), title=title)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return {"id": conversation.id, "thread_id": conversation.thread_id, "title": conversation.title}
    finally:
        db.close()


def list_conversations() -> list[dict]:
    db = SessionLocal()
    try:
        conversations = db.query(Conversation).order_by(Conversation.created_at.desc()).all()
        return [{"id": c.id, "thread_id": c.thread_id, "title": c.title} for c in conversations]
    finally:
        db.close()