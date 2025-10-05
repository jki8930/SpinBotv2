import secrets
import string
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import User, Prize, DailyPrize
from src.api.ws import manager
import datetime



async def get_or_create_daily_prize(session: AsyncSession) -> DailyPrize:
    today = datetime.date.today()
    stmt = select(DailyPrize).where(DailyPrize.date == today)
    result = await session.execute(stmt)
    daily_prize = result.scalar_one_or_none()

    if not daily_prize:
        daily_prize = DailyPrize(date=today)
        session.add(daily_prize)
        await session.commit()

    return daily_prize

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
        referred_by=referred_by,
        last_free_ticket_date=datetime.date.today()
    )
    session.add(new_user)
    await session.flush() # Use flush to get the new_user.id before committing

    if referred_by:
        referrer = await get_user_by_id(session, referred_by)
        if referrer:
            referrer.tickets += 1
            session.add(referrer)
            await manager.broadcast(f"{{\"type\": \"referral\", \"referrer_id\": {referrer.telegram_id}}}")

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

async def get_referrals(session: AsyncSession, user_id: int) -> list[User]:
    stmt = select(User).where(User.referred_by == user_id)
    result = await session.execute(stmt)
    return result.scalars().all()

async def get_top_users(session: AsyncSession, limit: int = 10) -> list[User]:
    stmt = select(User).order_by(User.balance.desc()).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()
