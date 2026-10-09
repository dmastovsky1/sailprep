"""FastAPI application factory. Run with `uvicorn sailprep_api.main:app`."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import __version__
from .config import get_settings
from .routes import boats, briefs, health, venues


def create_app() -> FastAPI:
    app = FastAPI(
        title="Sailprep API",
        version=__version__,
        description="Race-day weather briefs for sailors.",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=get_settings().cors_origins,
        allow_methods=["GET"],
        allow_headers=["*"],
    )
    app.include_router(health.router)
    app.include_router(boats.router)
    app.include_router(venues.router)
    app.include_router(briefs.router)
    return app


app = create_app()
