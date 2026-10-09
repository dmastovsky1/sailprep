"""FastAPI application factory. Run with `uvicorn sailprep_api.main:app`."""

from fastapi import FastAPI

from . import __version__
from .routes import health


def create_app() -> FastAPI:
    app = FastAPI(
        title="Sailprep API",
        version=__version__,
        description="Race-day weather briefs for sailors.",
    )
    app.include_router(health.router)
    return app


app = create_app()
