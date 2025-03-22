from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Waitlist(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    book_id: int = Field(foreign_key="book.id")
    user_id: int
    joined_at: datetime = Field(default_factory=datetime.now)
