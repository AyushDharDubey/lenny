from fastapi import APIRouter, Depends
from sqlmodel import Session
from lenny.models import LendingRecord
from lenny.schemas import LendingRecordCreate, LendingRecordRead
from lenny.models import get_session

router = APIRouter(prefix="/lending", tags=["Lending Records"])


@router.post("/", response_model=LendingRecordRead)
def borrow_book(lending: LendingRecordCreate, session: Session = Depends(get_session)):
    new_lending = LendingRecord(**lending.model_dump())
    session.add(new_lending)
    session.commit()
    session.refresh(new_lending)
    return new_lending
