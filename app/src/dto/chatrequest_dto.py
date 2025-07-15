from pydantic import BaseModel

class ChatRequestDTO(BaseModel):
    user_id: str
    message: str