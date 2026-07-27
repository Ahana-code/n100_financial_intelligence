from fastapi import FastAPI
from .routes import router

app = FastAPI(
    title="N100 Financial Intelligence API",
    description="Sprint 6 FastAPI Server",
    version="1.0.0"
)

app.include_router(router)