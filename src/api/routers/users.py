from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.api import schemas
from src.db import queries
from src.db.session import async_session

router = APIRouter()

async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

DBSession = Annotated[AsyncSession, Depends(get_db)]

@router.get("/users/{telegram_id}", response_model=schemas.User)
async def get_user(telegram_id: int, db: DBSession):
    user = await queries.get_user_by_telegram_id(db, telegram_id=telegram_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
