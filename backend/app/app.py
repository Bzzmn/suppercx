import os
from fastapi import FastAPI,HTTPException, Query, Request, Response
from dotenv import load_dotenv
import logging
from .routers import users, agents, tickets, ticketmessages, whatsapp
from .services.whatsapp_service import send_whatsapp_message

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="SupperCX API", version="0.1.0")
verification_token = os.getenv("WHATSAPP_VERIFICATION_TOKEN")

@app.get("/")
async def root():
    return {"message": "Welcome to SupperCX API"}

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(agents.router, prefix="/agents", tags=["agents"])
app.include_router(tickets.router, prefix="/tickets", tags=["tickets"])
app.include_router(ticketmessages.router, prefix="/ticketmessages", tags=["ticketmessages"])
app.include_router(whatsapp.router, prefix="/whatsapp", tags=["whatsapp"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
