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

async def send_text_message(to: str, content: str):
    async with httpx.AsyncClient() as client:
        try:
            payload = {
                "messaging_product": "whatsapp", 
                "recipient_type": "individual",
                "to": to, 
                "type": "text", 
                "text": {"body": content}
            }
            logger.info(f"Sending message to WhatsApp API: {payload}")
            response = await client.post(
                url, 
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }, 
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred: {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")
        

async def process_message(phone_number: str, message: str):
    pass
