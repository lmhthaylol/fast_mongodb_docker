from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient

url= "mongodb+srv://sonchuvan1104_db_user:Sonphong123@cluster0.hpj7o5k.mongodb.net/?appName=Cluster0"

client = AsyncIOMotorClient(url)

db = client.todo_db
collection_name = db["collection_name"]
key_collection = db["api_keys"]