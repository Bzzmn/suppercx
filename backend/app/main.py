import os
from fastapi import FastAPI, Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession # type: ignore
from sqlalchemy import select
from .database import get_db, engine
from .models import Base, User
from typing import List
import asyncio
from crewai import Agent, Task, Crew
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import logging

from utils.responseWhatsappMessage import send_text_message

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="SupperCX API", version="0.1.0", lifespan=lifespan)
verification_token = os.getenv("WHATSAPP_VERIFICATION_TOKEN")

#webhook de whatsapp + verificar el token
@app.get("/whatsapp_webhook")
async def verify_token(
    hub_mode: str = Query(..., alias="hub.mode"),
    hub_token: str = Query(..., alias="hub.verify_token"),
    hub_challenge: str = Query(..., alias="hub.challenge")
):
    if hub_mode == "subscribe" and hub_token == verification_token:
        return int(hub_challenge)
    raise HTTPException(status_code=403, detail="Verification token mismatch")

#Endpoint de whatsapp
@app.post("/whatsapp_webhook")
async def whatsapp_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    data = await request.json()
    
    try:
        entry = data['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        
        if 'messages' in value:
            message = value['messages'][0]
            contact = value['contacts'][0]
            
            phone_number = message['from']
            message_body = message['text']['body']
            timestamp = message['timestamp']
            name = contact['profile']['name']

            logger.info(f"Received message from {name} ({phone_number}): {message_body} at {timestamp}")
            
            try:
                response = await send_text_message(phone_number, "Hello! This is a response from SupperCX.")
                logger.info(f"Response sent: {response}")
                return {"status": "Message received and response sent"}
            except HTTPException as e:
                logger.error(f"Failed to send message: {e.detail}")
                return {"status": "Message received, but failed to send response", "error": e.detail}
        else:
            logger.info(f"Received non-message update: {value}")
            return {"status": "Update received"}
    except KeyError as e:
        logger.error(f"Error processing webhook data: {e}")
        logger.error(f"Received data: {data}")
        return {"status": "Error processing webhook data", "error": str(e)}

@app.get("/")
async def root():
    return {"message": "Welcome to SupperCX API"}

@app.get("/users/{user_id}", response_model=dict)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "phone": user.phone,
        "is_admin": user.is_admin
    }

@app.get("/users", response_model=List[dict])
async def read_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).offset(skip).limit(limit))
    users = result.scalars().all()
    return [
        {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone": user.phone,
            "is_admin": user.is_admin
        } for user in users
    ]

# Add more endpoints here for other models (Ticket, TicketMessage, Agent)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
