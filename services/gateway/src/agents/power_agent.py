import asyncio
from src.agents.base_agent import BaseAgent
from src.models.events import AgentMessage

class PowerAgent(BaseAgent):
    async def setup(self):
        # Subscribe to the power agent topic
        self.event_bus.subscribe("power_agent_topic", self.handle_message)

    async def handle_message(self, message: AgentMessage):
        payload = message.payload
        event_type = payload.get("type")
        
        if event_type == "iot_anomaly":
            sensor_id = payload.get("sensor_id")
            location_type = payload.get("location_type", "")
            reading = payload.get("reading", "")
            address = payload.get("address", "Unknown Location")
            
            print(f"[{self.name}] ⚡ Received IoT Anomaly from {sensor_id}: '{reading}'")
            
            # CRITICAL INFRASTRUCTURE CHECK
            if "hospital" in location_type.lower() or "hospital" in address.lower():
                print("\n" + "="*80)
                print("🚨 " * 10)
                print(f"[{self.name}] CRITICAL: Priority 1 Flag Set!")
                print(f"[{self.name}] DO NOT CUT POWER TO HOSPITAL GRID: {address}")
                print(f"[{self.name}] DEPLOYING BACKUP GENERATOR IMMEDIATELY")
                print("🚨 " * 10)
                print("="*80 + "\n")
                
                # Broadcast confirmation
                await self.publish(
                    topic="incident_updates",
                    payload={
                        "type": "resolution_update",
                        "incident_id": payload.get("incident_id"),
                        "status": "Priority 1 Handled",
                        "action": "Backup generator deployed to Hospital grid. Power cut blocked."
                    }
                )
            else:
                print(f"[{self.name}] ⚡ Assessing standard power anomaly at {location_type}.")
                await asyncio.sleep(1) # Simulate thinking
                print(f"[{self.name}] ⚡ Dispatching field crew to {address}.")
        else:
            print(f"[{self.name}] ⚡ Unhandled message type: {event_type}")
