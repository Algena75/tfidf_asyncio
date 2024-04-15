from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.endpoints.files import (csrf_error, internal_error,
                                     not_allowed_error, not_found_error)
from app.api.routers import main_router

exception_handlers = {
    404: not_found_error,
    500: internal_error,
    403: csrf_error,
    405: not_allowed_error
}

app = FastAPI(openapi_url=None, redoc_url=None,
              exception_handlers=exception_handlers)

app.include_router(main_router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
