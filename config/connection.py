
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = "mongodb+srv://sonchuvan1104_db_user:Sonphong123@cluster0.hpj7o5k.mongodb.net/?appName=Cluster0"
DATABASE_NAME = "college"

client = AsyncIOMotorClient(
    MONGO_URI,
    uuidRepresentation="standard" 
)

db = client[DATABASE_NAME]

book_collection = db.get_collection('books') 
key_collection = db.get_collection('api_keys')
users_collection = db.get_collection('users')