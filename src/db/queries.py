import secrets
import string
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import User, Prize

REFERRAL_BONUS = 100

async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def get_user_by_telegram_id(session: AsyncSession, telegram_id: int) -> User | None:
    stmt = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def get_user_by_referral_code(session: AsyncSession, referral_code: str) -> User | None:
    stmt = select(User).where(User.referral_code == referral_code)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

def generate_referral_code(length: int = 8) -> str:
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(length))

async def create_user(session: AsyncSession, telegram_id: int, username: str | None, referred_by: int | None = None) -> User:
    referral_code = generate_referral_code()
    while await get_user_by_referral_code(session, referral_code):
        referral_code = generate_referral_code()

    new_user = User(
        telegram_id=telegram_id, 
        username=username, 
        referral_code=referral_code,
        referred_by=referred_by
    )
    session.add(new_user)
    await session.flush() # Use flush to get the new_user.id before committing

    if referred_by:
        referrer = await get_user_by_id(session, referred_by)
        if referrer:
            referrer.balance += REFERRAL_BONUS
            session.add(referrer)

    await session.commit()
    return new_user

async def count_referrals(session: AsyncSession, user_id: int) -> int:
    stmt = select(func.count(User.id)).where(User.referred_by == user_id)
    result = await session.execute(stmt)
    return result.scalar() or 0

async def get_prizes(session: AsyncSession) -> list[Prize]:
    stmt = select(Prize)
    result = await session.execute(stmt)
    return result.scalars().all()
