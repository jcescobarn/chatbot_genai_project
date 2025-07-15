from fastapi import APIRouter
from models.chat_history import ChatHistory
from models.rag_engine import rag_engine 
from dto.chatrequest_dto import ChatRequestDTO
from dto.chatresponse_dto import ChatResponseDTO

router = APIRouter()

@router.post("/chat", response_model=dict)
def chat(request: ChatRequestDTO) -> dict:
    history = ChatHistory(request.user_id)
    history.append(f"User: {request.message}")

    raw_response = rag_engine.answer(request.message)

    if isinstance(raw_response, dict):
        message = raw_response.get("message", "Sin respuesta")
    elif isinstance(raw_response, str):
        message = raw_response
    else:
        message = str(raw_response)

    history.append(f"Bot: {message}")
    return dict(message=message)
