from fastapi import FastAPI
from app.routers import auth

app = FastAPI(
    title="Invoice Portal API",
    version="1.0.0"
)

app.include_router(auth.router)