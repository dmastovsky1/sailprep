"""Shared FastAPI dependencies."""

from sailprep.forecast import Fetcher, http_get_json


def get_fetcher() -> Fetcher:
    """The HTTP client used to reach forecast providers. Tests override this."""
    return http_get_json
