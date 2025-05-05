from fastapi import FastAPI
from app.onboard import router as onboard_router
from app.profile import router as profile_router
from app.match import router as match_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or ["*"] for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include routers
app.include_router(onboard_router, prefix="/onboard")
app.include_router(profile_router, prefix="/profile")
app.include_router(match_router, prefix="/match")
@app.get("/")
def read_root():
    return {"message": "VERA backend is running"}

