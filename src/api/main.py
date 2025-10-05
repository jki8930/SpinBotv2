from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.api.routers import users, wheel, referrals

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/frontend"), name="static")

app.include_router(users.router, prefix="/api")
app.include_router(wheel.router, prefix="/api")
app.include_router(referrals.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Hello from TRGSpin API"}
