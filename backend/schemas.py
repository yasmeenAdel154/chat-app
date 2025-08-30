# schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
# User

class UserCreate(BaseModel):
    username: str
    email: EmailStr
class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: Optional[datetime]

    class Config:
        from_attributes = True

# Interaction
class InteractionCreate(BaseModel):
    user_id: int
    user_input: str
    model_response: str

class InteractionRead(BaseModel):
    id: int
    user_id: int
    user_input: str
    model_response: str
    created_at: Optional[datetime]

    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    user_id: int
    message: str

class ChatResponse(BaseModel):
    interaction_id: int
    reply: str