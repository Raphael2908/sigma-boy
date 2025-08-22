import asyncio
import aiohttp
import json

async def test_mog():
    # Using one of your existing sample images
    image_path = "/Users/raphael/Develop/sigma-boy/Caleb.png"  # or "SleepyJoe.png"
    
    # Test parameters
    params = {
        "image": image_path,
        "prompt": "Analyze this person's jawline and provide improvement suggestions",
        "unique_key": "82d1de6e-bcab-4614-88ae-6cc8ce9cd4d7"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get("http://127.0.0.1:8000/mog", params=params) as response:
            print("Status Code:", response.status)
            # print("Response:", await response.json())

    return f"http://127.0.0.1:8000/evaluation/0c5ea485-4402-40d9-ace8-2823b62a587e/"

if __name__ == "__main__":
    asyncio.run(test_mog())
