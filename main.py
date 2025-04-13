from fastapi import FastAPI
from app.onboard import router as onboard_router

app = FastAPI()

app.include_router(onboard_router, prefix="/onboard")

@app.get("/")
def read_root():
    return {"message": "VERA backend is running"}
