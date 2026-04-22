from fastapi import FastAPI

# This is the "app" variable Uvicorn is looking for!
app = FastAPI(title="UrbanSync-AI Gateway")

@app.get("/")
def read_root():
    return {
        "message": "UrbanSync-AI is Online",
        "city": "Bengaluru",
        "status": "Ready for Hackathon"
    }