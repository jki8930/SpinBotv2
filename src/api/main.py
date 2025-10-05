from fastapi import FastAPI
from src.api.routers import users, wheel

app = FastAPI()

app.include_router(users.router, prefix="/api")
app.include_router(wheel.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Hello from TRGSpin API"}
