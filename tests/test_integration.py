import pytest
from httpx import ASGITransport, AsyncClient
from src.api.main import app
from src.db.models import User
from src.api.routers.users import get_db
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.db.session import init_db
import time

@pytest.mark.asyncio
async def test_integration(test_db_name):
    db_url = f"postgresql+asyncpg://postgres:postgres@localhost:5432/{test_db_name}"
    time.sleep(1)
    db_engine = create_async_engine(db_url, echo=True)
    await init_db(db_url)
    session_maker = async_sessionmaker(db_engine, expire_on_commit=False)

    async def override_get_db():
        async with session_maker() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. Create a new user
        async with session_maker() as session:
            new_user = User(telegram_id=123, username="test", balance=100, referral_code="test")
            session.add(new_user)
            await session.commit()

        # 2. Spin the wheel
        response = await ac.post("/api/wheel/spin/123")
        assert response.status_code == 200
        winning_prize = response.json()

        # 3. Check user's tickets
        response = await ac.get("/api/users/123")
        assert response.status_code == 200
        user_data = response.json()
        assert user_data["tickets"] == 0
        assert user_data["balance"] == 100 + winning_prize['amount']

        # 4. Check the leaderboard
        response = await ac.get("/api/users/top")
        assert response.status_code == 200
        leaderboard = response.json()
        assert len(leaderboard) > 0
        assert leaderboard[0]["telegram_id"] == 123

    await db_engine.dispose()
    time.sleep(1)