from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .models import AgentType, TicketState, Origin

class UserBase(BaseModel):
    first_name: str
    last_name: str
    mail: str
    username: str
    number: str

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    mail: Optional[str] = None
    username: Optional[str] = None
    number: Optional[str] = None

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True  # Usa esto en lugar de orm_mode = True

class AgentBase(BaseModel):
    type: AgentType

class AgentCreate(AgentBase):
    pass

class AgentUpdate(AgentBase):
    type: Optional[AgentType] = None

class AgentResponse(AgentBase):
    id: int

    class Config:
        from_attributes = True  # Usa esto en lugar de orm_mode = True

class TicketBase(BaseModel):
    title: str
    state: TicketState
    origin: Origin
    user_id: int
    agent_id: int

class TicketCreate(TicketBase):
    pass

class TicketUpdate(TicketBase):
    title: Optional[str] = None
    state: Optional[TicketState] = None
    origin: Optional[Origin] = None
    user_id: Optional[int] = None
    agent_id: Optional[int] = None

class TicketResponse(TicketBase):
    id: int
    created_at: datetime
    last_message_date: datetime

    class Config:
        from_attributes = True  # Usa esto en lugar de orm_mode = True

class TicketMessageBase(BaseModel):
    ticket_id: int
    conversation: str

class TicketMessageCreate(TicketMessageBase):
    pass

class TicketMessageUpdate(TicketMessageBase):
    conversation: Optional[str] = None

class TicketMessageResponse(TicketMessageBase):
    id: int

    class Config:
        from_attributes = True  # Usa esto en lugar de orm_mode = True
