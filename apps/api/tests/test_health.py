def test_health(client) -> None:
    r = client.get("/api/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["journal_mode"] == "wal"
    assert body["synchronous"] == "2"  # FULL
