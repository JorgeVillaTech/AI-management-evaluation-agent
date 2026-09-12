import uuid
from app.database import SessionLocal
from app.models.conversation import Conversation
from openai import OpenAI
import os


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


def generate_title(message: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": "Summarize this into a short, specific chat title (3-6 words, no quotes, no trailing punctuation). Always include the specific subject or company name mentioned, not just the general action."},
            {"role": "user", "content": message},
        ],
        max_tokens=20,
    )
    return response.choices[0].message.content.strip()


def rename_conversation(conversation_id: int, title: str) -> dict | None:
    db = SessionLocal()
    try:
        conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if conversation is None:
            return None
        conversation.title = title
        db.commit()
        db.refresh(conversation)
        return {"id": conversation.id, "thread_id": conversation.thread_id, "title": conversation.title}
    finally:
        db.close()


def delete_conversation(conversation_id: int) -> bool:
    db = SessionLocal()
    try:
        conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if conversation is None:
            return False
        db.delete(conversation)
        db.commit()
        return True
    finally:
        db.close()