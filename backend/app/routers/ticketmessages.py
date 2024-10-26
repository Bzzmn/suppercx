from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..database import get_db
from ..models import TicketMessage
from ..schemas import TicketMessageCreate, TicketMessageUpdate, TicketMessageResponse
from typing import List

router = APIRouter()

@router.post("/", response_model=TicketMessageResponse)
async def create_ticket_message(ticket_message: TicketMessageCreate, db: AsyncSession = Depends(get_db)):
    db_ticket_message = TicketMessage(**ticket_message.dict())
    db.add(db_ticket_message)
    await db.commit()
    await db.refresh(db_ticket_message)
    return db_ticket_message

@router.get("/", response_model=List[TicketMessageResponse])
async def read_ticket_messages(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TicketMessage).offset(skip).limit(limit))
    return result.scalars().all()

@router.get("/{message_id}", response_model=TicketMessageResponse)
async def read_ticket_message(message_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TicketMessage).filter(TicketMessage.id == message_id))
    message = result.scalar_one_or_none()
    if message is None:
        raise HTTPException(status_code=404, detail="Ticket message not found")
    return message

@router.put("/{message_id}", response_model=TicketMessageResponse)
async def update_ticket_message(message_id: int, ticket_message: TicketMessageUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TicketMessage).filter(TicketMessage.id == message_id))
    db_ticket_message = result.scalar_one_or_none()
    if db_ticket_message is None:
        raise HTTPException(status_code=404, detail="Ticket message not found")
    
    for key, value in ticket_message.dict(exclude_unset=True).items():
        setattr(db_ticket_message, key, value)
    
    await db.commit()
    await db.refresh(db_ticket_message)
    return db_ticket_message

@router.delete("/{message_id}", response_model=TicketMessageResponse)
async def delete_ticket_message(message_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TicketMessage).filter(TicketMessage.id == message_id))
    message = result.scalar_one_or_none()
    if message is None:
        raise HTTPException(status_code=404, detail="Ticket message not found")
    await db.delete(message)
    await db.commit()
    return message