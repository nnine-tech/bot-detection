# create_unique_index.py
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
MONGO_URI = os.getenv("MONGO_URL")
client = AsyncIOMotorClient(MONGO_URI)
db = client.get_database("botdetector")
features_collection = db["features"]

async def create_index():
    # Unique combination of ip + timestamp + endpoint
    await features_collection.create_index(
        [("ip", 1), ("timestamp", 1), ("endpoint", 1)],
        unique=True
    )
    print(" Unique index created on features collection!")

if __name__ == "__main__":
    asyncio.run(create_index())
