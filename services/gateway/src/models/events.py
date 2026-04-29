from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Any, Dict

def get_utc_now():
    return datetime.now(timezone.utc)

class AgentMessage(BaseModel):
    sender: str
    receiver_or_topic: str
    payload: Dict[str, Any]
    timestamp: datetime = Field(default_factory=get_utc_now)
    priority: int = 1
