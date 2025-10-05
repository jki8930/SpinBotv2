from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import Prize

async def seed_prizes(session: AsyncSession):
    prizes = [
        Prize(name="100", chance=0.5, amount=100),
        Prize(name="200", chance=0.2, amount=200),
        Prize(name="500", chance=0.1, amount=500),
        Prize(name="1000", chance=0.05, amount=1000),
        Prize(name="JACKPOT", chance=0.01, amount=10000),
        Prize(name="Пусто", chance=0.14, amount=0),
    ]
    session.add_all(prizes)
    await session.commit()
