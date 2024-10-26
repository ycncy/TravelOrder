from fastapi import FastAPI
from src.routers import trip

app = FastAPI()

app.include_router(trip.router)