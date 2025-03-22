from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class LendingRecordBase(BaseModel):
    book_id: int
    user_id: int


class LendingRecordCreate(LendingRecordBase):
    pass


class LendingRecordRead(LendingRecordBase):
    id: int
    borrowed_at: datetime
    due_date: datetime
    returned_at: Optional[datetime] = None

    class Config:
        from_attributes = True
