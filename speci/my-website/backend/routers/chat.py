"""
Chat router for the AI-Interactive Book backend
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from ..chat_service import chat_service

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = None
    selected_text: Optional[str] = None  # For selected-text-only QA
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    sources: List[str] = []

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    # Use the selected-text-only enforcement if text is selected
    if request.selected_text:
        result = chat_service.enforce_selected_text_qa(
            query=request.message,
            selected_text=request.selected_text
        )
    else:
        # Use standard QA with document retrieval
        result = chat_service.get_answer(
            query=request.message,
            context=request.context,
            user_id=request.user_id
        )

    return ChatResponse(
        response=result["response"],
        sources=result["sources"]
    )