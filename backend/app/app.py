import os
from fastapi import FastAPI,HTTPException, Query, Request, Depends
from dotenv import load_dotenv
import logging
from .routers import users, agents, tickets, ticketmessages
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db


# from utils.responseWhatsappMessage import send_text_message, process_message

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI(title="SupperCX API", version="0.1.0")
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

#             # Process the message and get a response
#             response = await process_message(phone_number, message_body)

#             # Send the response back to WhatsApp
#             await send_text_message(phone_number, response)

#             return {"status": "Message processed and response sent"}
#         else:
#             logger.info(f"Received non-message update: {value}")
#             return {"status": "Update received"}
#     except KeyError as e:
#         logger.error(f"Error processing webhook data: {e}")
#         logger.error(f"Received data: {data}")
#         return {"status": "Error processing webhook data", "error": str(e)}
#     except Exception as e:
#         logger.error(f"An unexpected error occurred: {str(e)}")
#         logger.error(f"Error type: {type(e).__name__}")
#         logger.exception("Full traceback:")
#         return {"status": "An unexpected error occurred", "error": str(e)}


@app.get("/")
async def root():
    return {"message": "Welcome to SupperCX API"}


app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(agents.router, prefix="/agents", tags=["agents"])
app.include_router(tickets.router, prefix="/tickets", tags=["tickets"])
app.include_router(
    ticketmessages.router, prefix="/ticketmessages", tags=["ticketmessages"]
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8003)
