from typing import Annotated, List
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from src.api import schemas
from src.db import queries
from src.api.routers.users import get_db

router = APIRouter()

DBSession = Annotated[AsyncSession, Depends(get_db)]

@router.get("/users/{telegram_id}/referrals", response_model=List[schemas.Referral])
async def get_referrals(telegram_id: int, db: DBSession):
    user = await queries.get_user_by_telegram_id(db, telegram_id=telegram_id)
    if user is None:
        return []
    referrals = await queries.get_referrals(db, user_id=user.id)
    return referrals
