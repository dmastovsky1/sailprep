"""Built-in boat class profiles.

Wind ranges are approximate guides for race planning, not class rules.
"""

from __future__ import annotations

from .models import Boat, BoatType

BOATS: dict[str, Boat] = {
    b.key: b
    for b in [
        # Dinghies
        Boat("ilca7", "ILCA 7 (Laser)", BoatType.DINGHY, 3, 30, 1, heavy_air_kt=20),
        Boat("ilca6", "ILCA 6 (Laser Radial)", BoatType.DINGHY, 3, 28, 1, heavy_air_kt=18),
        Boat("420", "420", BoatType.DINGHY, 3, 25, 2, heavy_air_kt=18),
        Boat("29er", "29er", BoatType.DINGHY, 4, 25, 2, heavy_air_kt=18),
        Boat("49er", "49er", BoatType.DINGHY, 4, 25, 2, heavy_air_kt=18),
        # Foilers
        Boat("waszp", "WASZP", BoatType.FOILER, 6, 25, 1, heavy_air_kt=18, foiling_kt=8),
        Boat(
            "moth", "International Moth", BoatType.FOILER, 5, 25, 1, heavy_air_kt=18, foiling_kt=7
        ),
        Boat("nacra17", "Nacra 17", BoatType.FOILER, 5, 25, 2, heavy_air_kt=18, foiling_kt=8),
        # Keelboats
        Boat("j70", "J/70", BoatType.KEELBOAT, 3, 25, 4, heavy_air_kt=18),
        Boat("etchells", "Etchells", BoatType.KEELBOAT, 3, 28, 3, heavy_air_kt=20),
        Boat("melges24", "Melges 24", BoatType.KEELBOAT, 3, 25, 5, heavy_air_kt=18),
        Boat("star", "Star", BoatType.KEELBOAT, 3, 30, 2, heavy_air_kt=20),
    ]
}


def get_boat(key: str) -> Boat:
    try:
        return BOATS[key.lower()]
    except KeyError:
        known = ", ".join(sorted(BOATS))
        raise ValueError(f"Unknown boat '{key}'. Known boats: {known}") from None
