from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from src.api.routers import users, wheel, referrals
from src.api.ws import manager

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/frontend"), name="static")

app.include_router(users.router, prefix="/api")
app.include_router(wheel.router, prefix="/api")
app.include_router(referrals.router, prefix="/api")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Message text was: {data}")
    except Exception:
        manager.disconnect(websocket)

@app.get("/")
async def root():
    return {"message": "Hello from TRGSpin API"}
