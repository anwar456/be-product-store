# app/db/database.py
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

client = None
db = None

async def connect_to_mongo():
    try:
        global client, db
        print("Connecting to MongoDB with URI:", MONGO_URI)   # debug
        client = AsyncIOMotorClient(MONGO_URI)
        db = client[MONGO_DB_NAME]
        print("✅ Connected to MongoDB! DB:", MONGO_DB_NAME)
    except Exception as e:
        print("❌ MongoDB Connection Error:", e)
        raise

async def close_mongo_connection():
    global client
    if client:
        client.close()
        print("❌ MongoDB connection closed")
