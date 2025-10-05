import secrets
import string
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import User

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
    await session.commit()
    return new_user
