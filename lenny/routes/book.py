from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from lenny.models import Book
from lenny.schemas import BookCreate, BookRead
from lenny.models import get_session

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=BookRead)
def create_book(book: BookCreate, session: Session = Depends(get_session)):
    new_book = Book(**book.model_dump())
    session.add(new_book)
    session.commit()
    session.refresh(new_book)
    return new_book


@router.get("/", response_model=list[BookRead])
def list_books(session: Session = Depends(get_session)):
    return session.exec(select(Book)).all()
