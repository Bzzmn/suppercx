import httpx
import os
from dotenv import load_dotenv
from fastapi import HTTPException
import logging

load_dotenv()

token = os.getenv("WHATSAPP_API_KEY")
url = os.getenv("WHATSAPP_URL")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def send_text_message(to: str, body: str):
    url = f"https://graph.facebook.com/v21.0/{os.getenv('WHATSAPP_PHONE_NUMBER_ID')}/messages"
    headers = {
        "Authorization": f"Bearer {os.getenv('WHATSAPP_API_KEY')}",
        "Content-Type": "application/json",
    }
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "text",
        "text": {"body": body or "Lo siento, no pude procesar tu mensaje."}  # Provide a default message
    }
    
    logging.info(f"Sending message to WhatsApp API: {data}")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP error occurred: {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

async def process_message(phone_number: str, message: str):
    pass
