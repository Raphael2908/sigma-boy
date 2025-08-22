import asyncio
import aiohttp
import json

async def test_mog():
    # Using one of your existing sample images
    image_path = "Caleb.png"  # or "SleepyJoe.png"
    
    # Test parameters
    params = {
        "image": image_path,
        "prompt": "Analyze this person's jawline and provide improvement suggestions",
        "job_id": "test_1"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get("http://127.0.0.1:8000/mog", params=params) as response:
            print("Status Code:", response.status)
            print("Response:", await response.json())

if __name__ == "__main__":
    asyncio.run(test_mog())
