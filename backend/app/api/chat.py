from fastapi import APIRouter

from app.models.ChatRequest import ChatRequest
from app.core.dependencies import chat_service

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/chat")
def chat(request: ChatRequest):
    return {
        "answer": chat_service.answer_question(request.question)
    }