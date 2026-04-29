from abc import ABC, abstractmethod
from core.event_bus import EventBus
from models.events import AgentMessage

class BaseAgent(ABC):
    def __init__(self, name: str, event_bus: EventBus):
        self.name = name
        self.event_bus = event_bus

    @abstractmethod
    async def setup(self):
        """Register subscriptions to the event bus here."""
        pass

    @abstractmethod
    async def handle_message(self, message: AgentMessage):
        """Process incoming messages."""
        pass

    async def publish(self, topic: str, payload: dict, priority: int = 1):
        message = AgentMessage(
            sender=self.name,
            receiver_or_topic=topic,
            payload=payload,
            priority=priority
        )
        await self.event_bus.publish(message)
