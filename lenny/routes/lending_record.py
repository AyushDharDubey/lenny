from fastapi import APIRouter, Depends
from sqlmodel import Session
from datetime import timedelta, datetime
from lenny.models import LendingRecord
from lenny.schemas import LendingRecordCreate, LendingRecordRead
from lenny.models import get_session

router = APIRouter(prefix="/lending", tags=["Lending Records"])


@router.post("/", response_model=LendingRecordRead)
def borrow_book(lending: LendingRecordCreate, session: Session = Depends(get_session)):
    lending_data = lending.model_dump()
    lending_data["borrow_date"] = datetime.now()
    lending_data["due_date"] = lending_data["borrow_date"] + timedelta(days=14)
    new_lending = LendingRecord(**lending_data)
    session.add(new_lending)
    session.commit()
    session.refresh(new_lending)
    return new_lending
