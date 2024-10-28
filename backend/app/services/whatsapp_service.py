import httpx
import os
from dotenv import load_dotenv
from fastapi import HTTPException
import logging
from app.cx_crew.src.crew import get_crew

load_dotenv()

whatsapp_token = os.getenv("WHATSAPP_API_KEY")
whatsapp_url = os.getenv("WHATSAPP_URL")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def send_whatsapp_message(to: str, body: str):
    url = whatsapp_url
    headers = {
        "Authorization": f"Bearer {whatsapp_token}",
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
    try:
        crew = get_crew()
        
        result = crew.kickoff(inputs={"query": message})
        
        response_text = result.raw if hasattr(result, 'raw') else str(result)
        
        await send_whatsapp_message(phone_number, response_text)
        
        return response_text
    except Exception as e:
        print(f"Error processing message: {str(e)}")
        await send_whatsapp_message(phone_number, "Lo siento, ocurrió un error al procesar tu mensaje.")
        raise
