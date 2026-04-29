import asyncio
import httpx

async def main():
    print("--- Starting Exotel Webhook Test ---")
    url = "http://localhost:8000/api/webhooks/exotel"
    
    # Exotel payload format (application/x-www-form-urlencoded)
    # Exotel sends a bunch of parameters, but we only care about From and Body here
    payload = {
        "From": "+919876543210",
        "To": "+911234567890",
        "Body": "Major water pipe burst outside my shop on 1st Avenue!"
    }
    
    print(f"Sending POST request to {url}")
    print(f"Payload: {payload}")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=payload)
            
        print(f"\nResponse Status Code: {response.status_code}")
        print(f"Response Body: {response.json()}")
        
    except httpx.ConnectError:
        print(f"\nError: Could not connect to {url}")
        print("Make sure your FastAPI server is running! (e.g. uvicorn src.main:app --reload)")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
