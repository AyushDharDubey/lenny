from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from lenny.models import Book
from lenny.schemas import BookCreate, BookRead
from lenny.models import get_session

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=BookRead)
def create_book(book: BookCreate, session: Session = Depends(get_session)):
    book_data = book.model_dump()
    book_data["available_copies"] = book_data["copies"]
    book_data["total_copies"] = book_data["copies"]
    del book_data["copies"]
    new_book = Book(**book_data)
    session.add(new_book)
    session.commit()
    session.refresh(new_book)
    return new_book


@router.get("/", response_model=list[BookRead])
def list_books(session: Session = Depends(get_session)):
    return session.exec(select(Book)).all()
