from fastapi import APIRouter
from app.services.conversation_service import create_conversation, list_conversations

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.get("")
async def get_conversations():
    return list_conversations()


@router.post("")
async def new_conversation():
    return create_conversation()