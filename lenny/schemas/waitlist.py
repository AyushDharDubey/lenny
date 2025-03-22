from pydantic import BaseModel
from datetime import datetime


class WaitlistBase(BaseModel):
    book_id: int
    user_id: int


class WaitlistCreate(WaitlistBase):
    pass


class WaitlistRead(WaitlistBase):
    id: int
    joined_at: datetime

    class Config:
        from_attributes = True
