from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    author: str
    isbn: str


class BookCreate(BookBase):
    copies: int


class BookRead(BookBase):
    id: int
    available_copies: int
    total_copies: int
    status: str
