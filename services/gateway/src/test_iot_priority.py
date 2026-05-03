import asyncio
import httpx
import json

async def trigger_hospital_anomaly():
    url = "http://localhost:8000/api/webhooks/iot/"
    payload = {
        "sensor_id": "METER-992",
        "location_type": "Hospital",
        "reading": "Grid voltage drop detected - 45% below baseline",
        "address": "City General Hospital"
    }

    print("🔌 Simulating IoT Smart Meter at City General Hospital...")
    print(f"Sending payload: {json.dumps(payload, indent=2)}")
    print("-" * 40)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=10.0)
            print(f"Response Status: {response.status_code}")
            print(f"Response Body: {response.json()}")
    except httpx.ConnectError:
        print("❌ Error: Could not connect to the server. Is FastAPI running on port 8000?")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(trigger_hospital_anomaly())
