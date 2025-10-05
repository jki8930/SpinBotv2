from pydantic import BaseModel

class UserBase(BaseModel):
    telegram_id: int
    username: str | None = None
    balance: int
    tickets: int

class User(UserBase):
    id: int
    referral_code: str

    class Config:
        from_attributes = True

class PrizeBase(BaseModel):
    name: str
    chance: float
    amount: int


class Prize(PrizeBase):
    id: int

    class Config:
        from_attributes = True

class Referral(UserBase):
    id: int

    class Config:
        from_attributes = True