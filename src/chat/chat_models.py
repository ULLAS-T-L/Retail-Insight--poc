from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class ChatRequest(BaseModel):
    message: str
    session_id: str

class ChatMessage(BaseModel):
    role: str
    message: str
    timestamp: str
    raw_data: Optional[str] = None

class ChatSessionResponse(BaseModel):
    session_id: str
    messages: List[ChatMessage]
