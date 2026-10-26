"""PUT /profile + the real GET /me.onboarding (S1, A8)."""

from __future__ import annotations

FULL = {"target_role": "intern", "track": "swe", "language": "python", "experience": "none"}


def test_fresh_user_not_onboarded(client) -> None:
    ob = client.get("/api/me").json()["onboarding"]
    assert ob == {"profile_done": False, "placement": "none"}


def test_profile_persists_and_marks_done(client) -> None:
    r = client.put("/api/profile", json={**FULL, "display_name": " Quan ", "tz": "UTC"})
    assert r.status_code == 200
    assert r.json()["onboarding"] == {"profile_done": True, "placement": "none"}
    me = client.get("/api/me").json()
    assert me["onboarding"]["profile_done"] is True
    s = me["settings"]
    assert (s["target_role"], s["track"], s["language"], s["experience"]) == (
        "intern", "swe", "python", "none",
    )  # fmt: skip
    assert s["display_name"] == "Quan" and s["tz"] == "UTC" and s["onboarded_at"]


def test_partial_profile_not_done_until_all_four(client) -> None:
    r = client.put("/api/profile", json={"target_role": "new_grad", "track": "ai"})
    assert r.json()["onboarding"]["profile_done"] is False
    r = client.put("/api/profile", json={"language": "python", "experience": "some"})
    assert r.json()["onboarding"]["profile_done"] is True
    assert client.get("/api/me").json()["settings"]["target_role"] == "new_grad"


def test_skip_flag_reported(client) -> None:
    r = client.put("/api/profile", json={**FULL, "placement": "skipped"})
    assert r.json()["onboarding"] == {"profile_done": True, "placement": "skipped"}
    assert client.get("/api/me").json()["onboarding"]["placement"] == "skipped"


def test_profile_validation(client) -> None:
    for bad in (
        {"target_role": "ceo"},
        {"track": "devops"},
        {"language": "java"},
        {"experience": "expert"},
        {"placement": "finished"},
    ):
        assert client.put("/api/profile", json=bad).status_code == 422
    r = client.put("/api/profile", json={"tz": "Mars/Base"})
    assert r.status_code == 422 and r.json()["error"]["code"] == "invalid_tz"
    assert client.get("/api/me").json()["onboarding"]["profile_done"] is False


def test_profile_idempotent(client) -> None:
    h = {"Idempotency-Key": "prof-1"}
    a = client.put("/api/profile", json=FULL, headers=h)
    b = client.put("/api/profile", json=FULL, headers=h)
    assert a.status_code == b.status_code == 200 and a.json() == b.json()
    # the replay did not re-apply: a different body under the same key returns the stored response
    c = client.put("/api/profile", json={**FULL, "track": "ai"}, headers=h)
    assert c.json() == a.json()
    assert client.get("/api/me").json()["settings"]["track"] == "swe"
