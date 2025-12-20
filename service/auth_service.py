from datetime import datetime, timedelta

from config.connection import db, token_collection


async def store_refresh_token(user_id: str, token: str):
    # = datetime.utcnow() + timedelta(days=expires_in_days)
    token_data = {
        "user_id": user_id,
        "refresh_token": token,
        #"expires_at": expires_at,
        "created_at": datetime.utcnow()
    }
    await token_collection.insert_one(token_data)