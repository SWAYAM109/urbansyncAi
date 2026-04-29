import asyncio
from agents.base_agent import BaseAgent
from models.events import AgentMessage

class TrafficAgent(BaseAgent):
    async def setup(self):
        self.event_bus.subscribe("traffic_agent", self.handle_message)

    async def handle_message(self, message: AgentMessage):
        payload = message.payload
        event_type = payload.get("type")
        
        if event_type == "diversion_request":
            location = payload.get("location", "Unknown Location")
            reason = payload.get("reason", "Unknown Reason")
            reply_to = payload.get("reply_to")
            
            print(f"[{self.name}] 🚦 Received diversion request at '{location}'. Reason: '{reason}'")
            print(f"[{self.name}] 🚦 Processing road closure and rerouting traffic...")
            
            await asyncio.sleep(2) # Simulate processing
            
            print(f"[{self.name}] 🚦 Road closed at {location}. Traffic rerouted successfully.")
            
            if reply_to:
                print(f"[{self.name}] 🚦 Sending acknowledgment to {reply_to}.")
                await self.publish(
                    topic=reply_to,
                    payload={
                        "type": "diversion_status",
                        "status": "active",
                        "location": location
                    }
                )
        else:
            print(f"[{self.name}] 🚦 Unhandled message type: {event_type}")
