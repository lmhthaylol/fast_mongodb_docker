from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = "mongodb+srv://sonchuvan1104_db_user:Sonphong123@cluster0.hpj7o5k.mongodb.net/?appName=Cluster0"
DATABASE_NAME = "book-model-db"

client = AsyncIOMotorClient(MONGO_URI)

db = client.college
book_collection = db.get_collection('books')
