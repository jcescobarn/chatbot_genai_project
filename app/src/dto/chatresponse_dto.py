from pydantic import BaseModel

class ChatResponseDTO(BaseModel):
    response: str