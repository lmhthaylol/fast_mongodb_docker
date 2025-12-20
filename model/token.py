from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

class UserToken(BaseModel):
    user_id: UUID
    refresh_token: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    #expires_at: datetime