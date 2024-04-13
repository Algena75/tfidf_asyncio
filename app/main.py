from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.routers import main_router

app = FastAPI()

app.include_router(main_router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
