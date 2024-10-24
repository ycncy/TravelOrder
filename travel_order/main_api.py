from fastapi import FastAPI
from src.routers import routes

app = FastAPI()

app.include_router(routes.router)