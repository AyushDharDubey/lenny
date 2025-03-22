from fastapi import APIRouter
from lenny.routes import book, lending_record, waitlist

router = APIRouter()


router.include_router(book.router)
router.include_router(lending_record.router)
router.include_router(waitlist.router)


@router.get("/")
async def home():
    return {"message": "Hello from Lenny API!", "status": "online"}
