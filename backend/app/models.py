from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base
import enum
import datetime


# Enums
class TicketState(enum.Enum):
    new = "new"
    open = "open"
    pending = "pending"
    closed = "closed"


class Origin(enum.Enum):
    email = "email"
    whatsapp = "whatsapp"


class AgentType(enum.Enum):
    human = "human"
    ia_agent = "ia_agent"


# Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    mail = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    number = Column(String, unique=True, nullable=False)


class Agent(Base):
    __tablename__ = "agents"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(AgentType), nullable=False)


class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    original_language = Column(String, nullable=False, default="English")
    state = Column(Enum(TicketState), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_message_date = Column(DateTime, default=datetime.datetime.utcnow)
    origin = Column(Enum(Origin), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    agent_id = Column(Integer, ForeignKey("agents.id"))
    user = relationship("User", backref="tickets")
    agent = relationship("Agent", backref="tickets")
    messages = relationship("TicketMessage", back_populates="ticket")


class TicketMessage(Base):
    __tablename__ = "ticket_messages"
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"))
    sender = Column(String, nullable=False)
    email = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    sent_date_time = Column(DateTime, default=datetime.datetime.utcnow)
    ticket = relationship("Ticket", back_populates="messages")
