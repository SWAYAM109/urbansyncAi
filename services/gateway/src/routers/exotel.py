from fastapi import APIRouter, Request
from typing import Optional

import sys
import os
# Hack to allow both 'from src.core' and 'from core' to work depending on how it's executed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.event_bus import EventBus
from models.events import AgentMessage

router = APIRouter()

# Global EventBus reference (will be set from main.py)
event_bus: Optional[EventBus] = None

def get_event_bus() -> EventBus:
    global event_bus
    if event_bus is None:
        raise RuntimeError("EventBus is not initialized")
    return event_bus

def triage_incident(message_body: str) -> dict:
    """
    Simple triage function to classify the text and extract a rough location.
    """
    text = message_body.lower()
    incident_type = "unknown"
    
    # Basic classification
    if "pipe" in text or "water" in text:
        incident_type = "pipe_burst"
    elif "power" in text or "electricity" in text:
        incident_type = "power_outage"
    elif "traffic" in text or "accident" in text:
        incident_type = "traffic_accident"
        
    # Basic location extraction (very rough, just for demo)
    location = "Unknown Location"
    if "on " in text:
        # Extract everything after "on " as location for demo
        parts = text.split("on ", 1)
        if len(parts) > 1:
            # removing punctuation from end
            location = parts[1].strip("!?. ")
            
    return {
        "type": incident_type,
        "description": message_body,
        "location": location
    }

@router.post("/exotel")
async def exotel_webhook(request: Request):
    """
    Exotel webhook endpoint. Exotel can send data as form-urlencoded.
    We accept the raw request and parse the form data.
    """
    print("\n--- [Webhook] Received incoming request from Exotel ---")
    
    # Exotel usually sends payload as Form data
    form_data = await request.form()
    
    # Extract 'From' number and 'Body' of the message
    sender_number = form_data.get("From", "Unknown Number")
    message_body = form_data.get("Body", "")
    
    print(f"--- [Webhook] Sender: {sender_number} | Message: '{message_body}' ---")
    
    # Triage the incident
    triage_result = triage_incident(message_body)
    print(f"--- [Webhook] Triage Result: Classified as '{triage_result['type']}' at '{triage_result['location']}' ---")
    
    # Publish to EventBus
    if triage_result["type"] == "pipe_burst":
        target_topic = "incident_water"
    elif triage_result["type"] == "power_outage":
        target_topic = "incident_power"
    else:
        target_topic = "incident_general"
        
    incident_message = AgentMessage(
        sender=f"Citizen-{sender_number}",
        receiver_or_topic=target_topic,
        payload={
            "type": "incident_report",
            "description": triage_result["description"],
            "location": triage_result["location"],
            "triage_class": triage_result["type"]
        }
    )
    
    bus = get_event_bus()
    print(f"--- [Webhook] Publishing incident to topic: '{target_topic}' ---")
    await bus.publish(incident_message)
    
    return {"status": "received", "triage": triage_result["type"]}
