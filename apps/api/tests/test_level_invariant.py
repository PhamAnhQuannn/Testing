"""The role level feeds readiness only: the learning path never depends on it (SPEC 5.7)."""

from __future__ import annotations

import pytest

LEVELS = ["intern", "fresher", "junior", "senior"]
FULL = {"track": "swe", "language": "python", "experience": "none"}


def _snapshot(client) -> tuple[bytes, bytes]:
    m, n = client.get("/api/map"), client.get("/api/next")
    assert m.status_code == 200 and n.status_code == 200 and m.content and n.content
    return m.content, n.content


@pytest.mark.parametrize("track", ["swe", "ai"])
def test_level_never_changes_map_or_next(client, track) -> None:
    assert (
        client.put(
            "/api/profile", json={**FULL, "track": track, "target_role": "intern"}
        ).status_code
        == 200
    )
    base = _snapshot(client)
    for level in LEVELS:
        assert client.put("/api/profile", json={"target_role": level}).status_code == 200
        # the chosen level is actually live (persisted to settings)...
        assert client.get("/api/me").json()["settings"]["target_role"] == level
        # ...and the readiness view does respond to it...
        diag = client.get(f"/api/diagnosis?role={track}-{level}")
        assert diag.status_code == 200 and diag.json()["role"]["key"] == f"{track}-{level}"
        # ...yet /map and /next are byte-identical regardless of level.
        assert _snapshot(client) == base
