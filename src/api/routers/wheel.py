from typing import Annotated, List
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.api import schemas
from src.db import queries
from src.api.routers.users import get_db
from src.api.ws import manager

router = APIRouter()

DBSession = Annotated[AsyncSession, Depends(get_db)]

@router.get("/wheel/prizes", response_model=List[schemas.Prize])
async def get_prizes(db: DBSession):
    prizes = await queries.get_prizes(db)
    return prizes

@router.post("/wheel/spin/{telegram_id}")
async def spin_wheel(telegram_id: int, db: DBSession):
    user = await queries.get_user_by_telegram_id(db, telegram_id=telegram_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    prizes = await queries.get_prizes(db)
    spin_cost = prizes[0].spin_cost if prizes else 100

    if user.balance < spin_cost:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    user.balance -= spin_cost

    total_chance = sum(p.chance for p in prizes)
    random_value = __import__("random").uniform(0, total_chance)
    winning_prize = None

    for prize in prizes:
        random_value -= prize.chance
        if random_value <= 0:
            winning_prize = prize
            break

    user.balance += winning_prize.amount
    await db.commit()

    await manager.broadcast(f"{{\"telegram_id\": {user.telegram_id}, \"balance\": {user.balance}}}")

    return winning_prize
