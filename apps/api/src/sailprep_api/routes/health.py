"""Liveness and readiness checks for the host and deploy pipeline."""

from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from .. import __version__
from ..db import get_session

router = APIRouter(tags=["health"])


class Health(BaseModel):
    status: str
    version: str


class Readiness(BaseModel):
    status: str
    database: str


@router.get("/health")
def health() -> Health:
    """The process is up. Does not touch the database."""
    return Health(status="ok", version=__version__)


@router.get("/health/ready", responses={503: {"model": Readiness}})
def ready(response: Response, session: Annotated[Session, Depends(get_session)]) -> Readiness:
    """The API can reach PostgreSQL and is ready for traffic."""
    try:
        session.execute(text("SELECT 1"))
    except SQLAlchemyError:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return Readiness(status="unavailable", database="unreachable")
    return Readiness(status="ok", database="ok")
