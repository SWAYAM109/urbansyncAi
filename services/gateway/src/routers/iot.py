from fastapi import APIRouter, HTTPException, Request, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
from src.core.event_bus import EventBus
import uuid

router = APIRouter()

# Global reference to be injected
event_bus: Optional[EventBus] = None

class IoTReading(BaseModel):
    sensor_id: str
    location_type: str
    reading: str
    address: Optional[str] = None

@router.post("/")
async def receive_iot_webhook(data: IoTReading, background_tasks: BackgroundTasks):
    if not event_bus:
        raise HTTPException(status_code=500, detail="EventBus not configured")
        
    print(f"[IOT WEBHOOK] Received payload from {data.sensor_id} at {data.location_type}")

    # Build the event payload
    payload = {
        "type": "iot_anomaly",
        "sensor_id": data.sensor_id,
        "location_type": data.location_type,
        "reading": data.reading,
        "address": data.address,
        "incident_id": f"INC-IOT-{str(uuid.uuid4())[:8].upper()}"
    }

    from src.models.events import AgentMessage
    
    msg = AgentMessage(
        sender="iot_system",
        receiver_or_topic="power_agent_topic",
        payload=payload
    )

    # Publish to power_agent_topic as an AgentMessage via background task to not block response
    background_tasks.add_task(
        event_bus.publish,
        msg
    )

    return {"status": "Accepted", "message": "IoT anomaly logged and dispatched"}
