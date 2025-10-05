from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import User

async def get_user_by_telegram_id(session: AsyncSession, telegram_id: int) -> User | None:
    stmt = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def create_user(session: AsyncSession, telegram_id: int, username: str | None) -> User:
    new_user = User(telegram_id=telegram_id, username=username)
    session.add(new_user)
    await session.commit()
    return new_user
