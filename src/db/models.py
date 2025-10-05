from sqlalchemy import BigInteger, String, ForeignKey, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    balance: Mapped[int] = mapped_column(default=0)
    referral_code: Mapped[str] = mapped_column(String, unique=True, index=True)
    referred_by: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)

class Prize(Base):
    __tablename__ = 'prizes'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    chance: Mapped[float] = mapped_column(Float)
    amount: Mapped[int] = mapped_column()
