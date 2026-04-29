import asyncio
from agents.base_agent import BaseAgent
from models.events import AgentMessage

class WaterAgent(BaseAgent):
    async def setup(self):
        # Subscribe to incident alerts and direct messages
        self.event_bus.subscribe("incident_water", self.handle_message)
        self.event_bus.subscribe("water_agent", self.handle_message)

    async def handle_message(self, message: AgentMessage):
        payload = message.payload
        event_type = payload.get("type")
        
        if event_type == "incident_report":
            incident_desc = payload.get("description", "Unknown incident")
            print(f"[{self.name}] 💧 Received incident report: '{incident_desc}'")
            
            if "pipe burst" in incident_desc.lower():
                print(f"[{self.name}] 💧 Assessing incident...")
                await asyncio.sleep(1) # Simulate thinking
                print(f"[{self.name}] 💧 Assessment complete: Need to dig up the road.")
                
                # Request traffic diversion
                print(f"[{self.name}] 💧 Requesting road closure and traffic diversion from TrafficAgent.")
                await self.publish(
                    topic="traffic_agent",
                    payload={
                        "type": "diversion_request",
                        "location": payload.get("location", "Unknown Location"),
                        "reason": "Major Pipe Burst - Road excavation required",
                        "reply_to": "water_agent"
                    }
                )
        elif event_type == "diversion_status":
            status = payload.get("status")
            print(f"[{self.name}] 💧 Received update from {message.sender}: Traffic diversion status is '{status}'. Proceeding with repair.")
        else:
            print(f"[{self.name}] 💧 Unhandled message type: {event_type}")
