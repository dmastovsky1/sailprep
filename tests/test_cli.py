from sailprep.cli import main


def test_brief_with_geocoding(fake_fetch, capsys):
    rc = main(
        ["brief", "--venue", "Newport", "--boat", "j70", "--date", "2026-07-18"], fetch=fake_fetch
    )
    out = capsys.readouterr().out
    assert rc == 0
    assert out.startswith("# Race Brief: Newport, Rhode Island, United States")
    assert "J/70" in out
    assert "| 11:00 |" in out and "| 16:00 |" in out
    assert len(fake_fetch.calls) == 2


def test_brief_with_coordinates_skips_geocoding(fake_fetch, tmp_path):
    out = tmp_path / "brief.md"
    rc = main(
        [
            "brief",
            "--venue",
            "Narragansett Bay",
            "--lat",
            "41.49",
            "--lon",
            "-71.33",
            "--boat",
            "waszp",
            "--date",
            "2026-07-18",
            "-o",
            str(out),
        ],
        fetch=fake_fetch,
    )
    assert rc == 0
    assert len(fake_fetch.calls) == 1
    assert "# Race Brief: Narragansett Bay" in out.read_text()


def test_unknown_boat_returns_error(fake_fetch, capsys):
    rc = main(["brief", "--venue", "X", "--boat", "nope"], fetch=fake_fetch)
    assert rc == 2
    assert "Unknown boat" in capsys.readouterr().err


def test_boats_lists_all_types(capsys):
    assert main(["boats"]) == 0
    out = capsys.readouterr().out
    for t in ("dinghy", "foiler", "keelboat"):
        assert t in out
