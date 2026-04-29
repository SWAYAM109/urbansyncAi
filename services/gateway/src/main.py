import sys
import os

# Ensure the src directory is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from src.core.rag_engine import RAGEngine
from src.core.event_bus import EventBus
from src.agents.water_agent import WaterAgent
from src.agents.traffic_agent import TrafficAgent
from src.routers import exotel
from pydantic import BaseModel

global_event_bus = EventBus()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("--- Starting UrbanSync-AI Gateway ---")
    global_event_bus.start()
    
    # Initialize agents
    water_agent = WaterAgent(name="WaterAgent", event_bus=global_event_bus)
    traffic_agent = TrafficAgent(name="TrafficAgent", event_bus=global_event_bus)
    
    await water_agent.setup()
    await traffic_agent.setup()
    
    # Inject event_bus into router
    exotel.event_bus = global_event_bus
    
    print("--- EventBus and Agents Initialized ---")
    yield
    # Shutdown
    print("--- Shutting down UrbanSync-AI Gateway ---")
    await global_event_bus.stop()

# This is the "app" variable Uvicorn is looking for!
app = FastAPI(title="UrbanSync-AI Gateway", lifespan=lifespan)
rag = RAGEngine()

# Add Exotel router
app.include_router(exotel.router, prefix="/api/webhooks")

# Schema for incoming search requests
class QueryRequest(BaseModel):
    text: str

@app.get("/")
def root():
    return {"status": "Active", "engine": "UrbanSync-RAG-v1"}

@app.post("/get-sop")
async def get_sop(request: QueryRequest):
    """
    This endpoint will be called by your 'Agents' 
    whenever an incident is reported.
    """
    try:
        procedures = rag.query_sop(request.text)
        if not procedures:
            raise HTTPException(status_code=404, detail="No relevant SOP found")
        return {"incident": request.text, "steps": procedures}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))