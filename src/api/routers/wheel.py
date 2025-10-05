from typing import Annotated, List
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from src.api import schemas
from src.db import queries
from src.api.routers.users import get_db

router = APIRouter()

DBSession = Annotated[AsyncSession, Depends(get_db)]

@router.get("/wheel/prizes", response_model=List[schemas.Prize])
async def get_prizes(db: DBSession):
    prizes = await queries.get_prizes(db)
    return prizes
