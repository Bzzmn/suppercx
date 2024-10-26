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
import os

load_dotenv()



app = FastAPI(title="SupperCX API", version="0.1.0")
verification_token = os.getenv("WHATSAPP_VERIFICATION_TOKEN")

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
    phone_number = data.get('from')
    message = data.get('message')

    if not phone_number or not message:
        raise HTTPException(status_code=400, detail="Invalid request format")
    
    print(data)
    return {"message": "Whatsapp webhook received"}


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="SupperCX API", version="0.1.0", lifespan=lifespan)

# Remove the old @app.on_event("startup") function

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
