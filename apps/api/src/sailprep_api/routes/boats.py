"""Built-in boat class profiles."""

from fastapi import APIRouter
from sailprep.boats import BOATS
from sailprep.models import Boat

from ..schemas import BoatClassOut

router = APIRouter(prefix="/api/v1", tags=["boats"])


def boat_out(b: Boat) -> BoatClassOut:
    return BoatClassOut(
        key=b.key,
        name=b.name,
        type=b.type.value,
        crew=b.crew,
        min_wind_kt=b.min_wind_kt,
        max_wind_kt=b.max_wind_kt,
        heavy_air_kt=b.heavy_air_kt,
        foiling_kt=b.foiling_kt,
    )


@router.get("/boat-classes")
def list_boat_classes() -> list[BoatClassOut]:
    """Every built-in boat class, grouped by type then name."""
    order = {"dinghy": 0, "foiler": 1, "keelboat": 2}
    boats = sorted(BOATS.values(), key=lambda b: (order[b.type.value], b.name))
    return [boat_out(b) for b in boats]
