from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from ..database import get_db
from ..models import Ticket, TicketState, Origin
from ..schemas import TicketCreate, TicketUpdate, TicketResponse, TicketMessageResponse
from typing import List

router = APIRouter()


@router.post("/", response_model=TicketResponse)
async def create_ticket(ticket: TicketCreate, db: AsyncSession = Depends(get_db)):
    db_ticket = Ticket(**ticket.dict())
    db.add(db_ticket)
    await db.commit()
    await db.refresh(db_ticket)
    return db_ticket


@router.get("/", response_model=List[TicketResponse])
async def read_tickets(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Ticket)
        .options(joinedload(Ticket.messages))
        .offset(skip)
        .limit(limit)
    )
    tickets = result.unique().scalars().all()
    
    return [
        TicketResponse(
            id=ticket.id,
            title=ticket.title,
            description=ticket.description,
            original_language=ticket.original_language,
            status=ticket.state.value,
            source=ticket.origin.value,
            messages=[
                TicketMessageResponse(
                    id=message.id,
                    sender=message.sender,
                    email=message.email,
                    body=message.body,
                    sent_date_time=message.sent_date_time
                ) for message in ticket.messages
            ]
        ) for ticket in tickets
    ]


@router.get("/{ticket_id}", response_model=TicketResponse)
async def read_ticket(ticket_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Ticket).filter(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.put("/{ticket_id}", response_model=TicketResponse)
async def update_ticket(
    ticket_id: int, ticket: TicketUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Ticket).filter(Ticket.id == ticket_id))
    db_ticket = result.scalar_one_or_none()
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    for key, value in ticket.dict(exclude_unset=True).items():
        setattr(db_ticket, key, value)

    await db.commit()
    await db.refresh(db_ticket)
    return db_ticket


@router.delete("/{ticket_id}", response_model=TicketResponse)
async def delete_ticket(ticket_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Ticket).filter(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    await db.delete(ticket)
    await db.commit()
    return ticket
