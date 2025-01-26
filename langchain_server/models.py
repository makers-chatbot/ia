from dataclasses import dataclass
from typing import Optional
from pydantic import BaseModel


@dataclass
class Product:
    name: str
    description: str
    price: float


class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    message: str
