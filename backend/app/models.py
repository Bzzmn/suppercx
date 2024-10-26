from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), index=True)
    last_name = Column(String(50), index=True)
    email = Column(String(100), unique=True, index=True)
    phone = Column(String(20), unique=True, index=True)
    hashed_password = Column(String(100))
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tickets = relationship("Ticket", back_populates="user")

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    agent_id = Column(Integer, ForeignKey("agents.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = Column(Enum("new", "open", "pending", "closed", name="ticket_status"), default="new")
    title = Column(String(100), index=True)
    origin = Column(String(50), index=True)

    user = relationship("User", back_populates="tickets")
    agent = relationship("Agent", back_populates="tickets")
    messages = relationship("TicketMessage", back_populates="ticket")

class TicketMessage(Base):
    __tablename__ = "ticket_messages"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"))
    sender_id = Column(Integer, ForeignKey("users.id"))  # Puede ser usuario o agente
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_from_customer = Column(Boolean, default=True)

    ticket = relationship("Ticket", back_populates="messages")
    sender = relationship("User")

class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    description = Column(String(255))
    type = Column(Enum("ai_assistant", "human", name="agent_type"), default="ai_assistant")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tickets = relationship("Ticket", back_populates="agent")
