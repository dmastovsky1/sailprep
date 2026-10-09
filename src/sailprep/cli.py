"""Command-line entry point: `sailprep brief ...`."""

from __future__ import annotations

import argparse
import sys
from datetime import date, datetime, time
from pathlib import Path

from . import __version__
from .analysis import summarize
from .boats import BOATS, get_boat
from .brief import render_markdown
from .forecast import Fetcher, geocode, get_hourly, http_get_json
from .models import RaceDay, Venue


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="sailprep", description=__doc__)
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("boats", help="List built-in boat classes")

    b = sub.add_parser("brief", help="Generate a race brief")
    b.add_argument("--venue", required=True, help="Venue name, e.g. 'Newport, RI'")
    b.add_argument("--lat", type=float, help="Latitude (skips geocoding)")
    b.add_argument("--lon", type=float, help="Longitude (skips geocoding)")
    b.add_argument("--boat", required=True, help="Boat class key (see `sailprep boats`)")
    b.add_argument(
        "--date",
        type=date.fromisoformat,
        default=date.today(),
        help="Race date YYYY-MM-DD (default today)",
    )
    b.add_argument(
        "--start",
        type=time.fromisoformat,
        default=time(11, 0),
        help="First warning signal HH:MM (default 11:00)",
    )
    b.add_argument(
        "--end",
        type=time.fromisoformat,
        default=time(16, 0),
        help="Last race finish HH:MM (default 16:00)",
    )
    b.add_argument("-o", "--output", type=Path, help="Write Markdown here instead of stdout")
    return p


def run_brief(args: argparse.Namespace, fetch: Fetcher = http_get_json) -> str:
    boat = get_boat(args.boat)
    if args.lat is not None and args.lon is not None:
        venue = Venue(args.venue, args.lat, args.lon)
    else:
        venue = geocode(args.venue, fetch)
    race = RaceDay(
        venue=venue,
        boat=boat,
        start=datetime.combine(args.date, args.start),
        end=datetime.combine(args.date, args.end),
    )
    race.hours = get_hourly(venue, args.date, fetch)
    return render_markdown(race, summarize(race))


def main(argv: list[str] | None = None, fetch: Fetcher = http_get_json) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "boats":
        for key, b in sorted(BOATS.items()):
            print(f"{key:10} {b.name:24} {b.type.value:9} {b.min_wind_kt:g}-{b.max_wind_kt:g} kt")
        return 0
    try:
        md = run_brief(args, fetch)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    if args.output:
        args.output.write_text(md)
        print(f"Wrote {args.output}")
    else:
        print(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
