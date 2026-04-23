from fastapi import FastAPI, HTTPException
from src.core.rag_engine import RAGEngine
from pydantic import BaseModel

# This is the "app" variable Uvicorn is looking for!
app = FastAPI(title="UrbanSync-AI Gateway")
rag = RAGEngine()

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