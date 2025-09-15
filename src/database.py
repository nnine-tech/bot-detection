import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URL")
PORT = os.getenv("PORT") 

if not MONGO_URI:
    raise ValueError(" MONGO_URL not found in .env")

# Initialize client & database
client = AsyncIOMotorClient(MONGO_URI)

# Extract database name from URI dynamically
db_name = MONGO_URI.rsplit("/", 1)[-1].split("?")[0]  # gets 'botdetector'
db = client.get_database(db_name)

# Collections
logs_collection = db["logs"]
features_collection = db["features"]
predictions_collection = db["predictions"]

# Test connection
async def test_connection():
    try:
        await client.admin.command("ping")
        collections = await db.list_collection_names()
        print(f" MongoDB connected successfully to '{db_name}'!")
        print(f" Collections: {collections}")
        print(f"(server running on: {PORT} )")
    except Exception as e:
        print(" MongoDB connection failed:", e)
        raise e

# Optional: run test when executing this file directly
if __name__ == "__main__":
    asyncio.run(test_connection())
