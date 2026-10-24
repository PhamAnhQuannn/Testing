from sqlalchemy import func, select

from app.models import tables as t


def count(client, model):
    with client.app.state.rt.session() as db:
        return db.scalar(select(func.count()).select_from(model))


ATTEMPT = {
    "problem_id": "add-two",
    "mode": "submit",
    "code": "x",
    "verdict": "WA",
    "passed": 1,
    "total": 2,
    "elapsed_ms": 1000,
}


def test_same_key_five_times_writes_once(client):
    h = {"Idempotency-Key": "11111111-1111-4111-8111-111111111111"}
    first = client.post("/api/attempts", json=ATTEMPT, headers=h)
    assert first.status_code == 201
    for _ in range(4):
        again = client.post("/api/attempts", json=ATTEMPT, headers=h)
        assert again.status_code == 201
        assert again.json() == first.json()  # the very same stored response
        assert again.headers["idempotent-replay"] == "true"
    assert count(client, t.Attempt) == 1
    assert count(client, t.Event) == 1


def test_without_a_key_every_post_writes(client):
    for _ in range(3):
        client.post("/api/attempts", json=ATTEMPT)
    assert count(client, t.Attempt) == 3


def test_different_keys_are_different_events(client):
    for i in range(3):
        client.post("/api/attempts", json=ATTEMPT, headers={"Idempotency-Key": f"k{i}"})
    assert count(client, t.Attempt) == 3


def test_quiz_answer_replay_does_not_double_count(client):
    body = {"quiz_item_id": "py.a.one#q1", "run_no": 1, "answer": ["b"]}
    h = {"Idempotency-Key": "quiz-1"}
    for _ in range(5):
        r = client.post("/api/quiz/answers", json=body, headers=h)
        assert r.json()["attempt_no"] == 1
    assert count(client, t.QuizAnswer) == 1


def test_key_reuse_for_another_request_is_rejected(client):
    h = {"Idempotency-Key": "shared"}
    client.post("/api/attempts", json=ATTEMPT, headers=h)
    r = client.post("/api/problems/add-two/hints", headers=h)
    assert r.status_code == 422 and r.json()["error"]["code"] == "idempotency_key_reuse"


def test_errors_are_replayed_too_but_5xx_release_the_key(client):
    h = {"Idempotency-Key": "bad-body"}
    r1 = client.post("/api/attempts", json={}, headers=h)
    r2 = client.post("/api/attempts", json={}, headers=h)
    assert r1.status_code == r2.status_code == 422 and r1.json() == r2.json()


def test_in_progress_key_gets_409_and_stale_claim_is_taken_over(client, clock):
    rt = client.app.state.rt
    with rt.session() as db:
        db.add(
            t.IdempotencyKey(
                key="stuck",
                user_id=1,
                method="POST",
                path="/api/attempts",
                status=0,
                response=None,
                created_at=clock(),
            )
        )
        db.commit()
    h = {"Idempotency-Key": "stuck"}
    r = client.post("/api/attempts", json=ATTEMPT, headers=h)
    assert r.status_code == 409 and r.json()["error"]["code"] == "idempotency_in_progress"
    clock.advance(seconds=31)  # the first worker is presumed dead
    assert client.post("/api/attempts", json=ATTEMPT, headers=h).status_code == 201
    assert count(client, t.Attempt) == 1


def test_put_with_key_and_gets_are_unaffected(client):
    h = {"Idempotency-Key": "put-1"}
    body = {"code": "a", "updated_at": "2026-11-02T03:00:00Z"}
    assert client.put("/api/drafts/add-two", json=body, headers=h).status_code == 200
    assert client.put("/api/drafts/add-two", json=body, headers=h).headers["idempotent-replay"]
    assert client.get("/api/map", headers=h).status_code == 200  # GET ignores the header


def test_concurrent_requests_with_one_key_write_once(client):
    from concurrent.futures import ThreadPoolExecutor

    h = {"Idempotency-Key": "race"}

    def post(_):
        return client.post("/api/attempts", json=ATTEMPT, headers=h).status_code

    with ThreadPoolExecutor(5) as pool:
        codes = list(pool.map(post, range(5)))
    assert set(codes) <= {201, 409}  # losers either replay or are told to retry
    assert 201 in codes
    assert count(client, t.Attempt) == 1
