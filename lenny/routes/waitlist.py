from fastapi import APIRouter, Depends
from sqlmodel import Session
from lenny.models import Waitlist
from lenny.schemas import WaitlistCreate, WaitlistRead
from lenny.models import get_session

router = APIRouter(prefix="/waitlist", tags=["Waitlist"])


@router.post("/", response_model=WaitlistRead)
def join_waitlist(entry: WaitlistCreate, session: Session = Depends(get_session)):
    new_entry = Waitlist(**entry.model_dump())
    session.add(new_entry)
    session.commit()
    session.refresh(new_entry)
    return new_entry
