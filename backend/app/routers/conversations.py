from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.conversation_service import create_conversation, list_conversations, rename_conversation, delete_conversation, generate_title


router = APIRouter(prefix="/conversations", tags=["conversations"])

class RenameRequest(BaseModel):
    title: str

class TitleRequest(BaseModel):
    message: str


@router.get("")
async def get_conversations():
    return list_conversations()

@router.post("")
async def new_conversation():
    return create_conversation()

@router.patch("/{conversation_id}")
async def rename_conversation_endpoint(conversation_id: int, body: RenameRequest):
    updated = rename_conversation(conversation_id, body.title)
    if updated is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return updated

@router.delete("/{conversation_id}")
async def delete_conversation_endpoint(conversation_id: int):
    deleted = delete_conversation(conversation_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"status": "deleted"}

@router.post("/{conversation_id}/generate-title")
async def generate_title_endpoint(conversation_id: int, body: TitleRequest):
    title = generate_title(body.message)
    updated = rename_conversation(conversation_id, title)
    if updated is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return updated