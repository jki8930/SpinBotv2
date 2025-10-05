from fastapi import FastAPI
from src.api.routers import users

app = FastAPI()

app.include_router(users.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Hello from TRGSpin API"}
