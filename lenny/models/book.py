from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum


class BookStatus(str, Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"


class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author: str
    isbn: str
    available_copies: int
    total_copies: int
    status: BookStatus = Field(default=BookStatus.AVAILABLE)
