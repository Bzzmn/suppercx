from fastapi import APIRouter, HTTPException, Query, Request, Response
from app.services.whatsapp_service import send_whatsapp_message, process_message
import os
import asyncio

router = APIRouter()

verification_token = os.getenv("WHATSAPP_VERIFICATION_TOKEN")

# Use a dictionary to store processed message IDs
processed_messages = {}

@router.get("/webhook")
async def verify_token(
    hub_mode: str = Query(..., alias="hub.mode"),
    hub_token: str = Query(..., alias="hub.verify_token"),
    hub_challenge: str = Query(..., alias="hub.challenge")
):
    if hub_mode == "subscribe" and hub_token == verification_token:
        print(f"Verification token: {verification_token}")
        return int(hub_challenge)
    raise HTTPException(status_code=403, detail="Verification token mismatch")

@router.post("/webhook")
async def whatsapp_webhook(request: Request):
    body = await request.json()
    
    # Extract the message ID
    try:
        message_id = body['entry'][0]['changes'][0]['value']['messages'][0]['id']
        sender = body['entry'][0]['changes'][0]['value']['messages'][0]['from']
        text = body['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
    except (KeyError, IndexError):
        return Response(status_code=200)  # Acknowledge receipt even if we can't process it

    # Check if we've already processed this message
    if message_id in processed_messages:
        print(f"Duplicate message received: {message_id}")
        return Response(status_code=200)  # Acknowledge receipt of duplicate

    # Mark this message as processed
    processed_messages[message_id] = True

    # Process the message
    try:
        response = await process_message(sender, text)
        print(f"Processed message: {message_id}")
        
        # Optionally, you can clean up old message IDs to prevent memory growth
        if len(processed_messages) > 1000:  # Adjust this number as needed
            oldest_key = next(iter(processed_messages))
            del processed_messages[oldest_key]
        
        return Response(content=response, status_code=200)
    except Exception as e:
        print(f"Error processing message: {str(e)}")
        return Response(status_code=500)
