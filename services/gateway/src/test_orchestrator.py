import asyncio
import sys
import os

# Ensure the src directory is in the path so we can import modules correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.event_bus import EventBus
from agents.water_agent import WaterAgent
from agents.traffic_agent import TrafficAgent
from models.events import AgentMessage

async def main():
    print("--- UrbanSync AI Orchestrator Starting ---")
    
    # 1. Initialize Event Bus
    event_bus = EventBus()
    event_bus.start()
    
    # 2. Register Agents
    water_agent = WaterAgent(name="WaterAgent", event_bus=event_bus)
    traffic_agent = TrafficAgent(name="TrafficAgent", event_bus=event_bus)
    
    await water_agent.setup()
    await traffic_agent.setup()
    
    print("\n--- Simulating Incident: Major Pipe Burst on 1st Avenue ---\n")
    
    # 3. Inject the Incident
    incident_message = AgentMessage(
        sender="SystemOrchestrator",
        receiver_or_topic="incident_water",
        payload={
            "type": "incident_report",
            "description": "Major Pipe Burst on 1st Avenue",
            "location": "1st Avenue"
        }
    )
    
    await event_bus.publish(incident_message)
    
    # 4. Allow the simulation to run for a few seconds to process all events
    await asyncio.sleep(5)
    
    print("\n--- Shutting down Orchestrator ---")
    await event_bus.stop()

if __name__ == "__main__":
    asyncio.run(main())
