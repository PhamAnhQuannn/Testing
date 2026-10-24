import json

from fastapi.testclient import TestClient

from app.config import REPO_ROOT, Settings
from app.main import create_app
from app.runtime import Runtime
from app.services.content_loader import ContentStore


def test_map(client):
    m = client.get("/api/map").json()
    ids = [s["id"] for s in m["subtopics"]]
    assert ids == ["py.a.one", "py.a.two", "py.a.three"]  # plan order
    one, two, three = m["subtopics"]
    assert one["unlocked"] and one["status"] == "unlocked" and one["score"] == 0
    assert not two["unlocked"] and two["status"] == "locked"
    assert two["lock_reasons"] == [
        {"prerequisite": "py.a.one", "score": 0, "need": 2, "name_vi": "Mục py.a.one"}
    ]
    # a prerequisite outside the content and not assumed
    assert three["lock_reasons"][1]["missing_content"] is True
    assert one["content_status"] == "published" and one["has_lesson"]
    assert two["content_status"] == "none"
    assert m["assumed"] == ["cs.assumed"]
    assert m["due_cards"] == 0


def test_lesson_public_view_has_no_secrets(client):
    r = client.get("/api/lessons/py.a.one")
    assert r.status_code == 200
    text = r.text
    assert "def f(): return 1" not in text  # code_exercise solution
    lesson = r.json()
    blocks = {b["id"]: b for b in lesson["blocks"]}
    assert "answer" not in blocks["q1"] and "explain_md" not in blocks["q1"]
    assert "expected_output" not in blocks["q4"]
    assert blocks["q3"]["blanks"] == [{"index": 0}]
    assert blocks["ex1"]["starter"] and "solution" not in blocks["ex1"]
    assert lesson["progress"] == {
        "run_no": 1,
        "answers": {},
        "lesson_done": False,
        "quiz_best": None,
        "score": 0,
        "known_basic": False,
    }
    assert client.get("/api/lessons/py.a.two").status_code == 404
    assert client.get("/api/lessons/nope").json()["error"]["code"] == "lesson_not_found"


def test_problem_public_view(client):
    p = client.get("/api/problems/add-two").json()
    assert p["sample_tests"] == [{"id": "s1", "args": [1, 2], "expected": 3}]
    assert p["hints"] == [] and p["hints_used"] == 0 and p["hint_count"] == 3
    assert p["starter"]["python"].startswith("def add")
    assert p["status"] == "todo" and p["last_attempt"] is None
    assert not {"solution", "tests", "brute", "hidden"} & set(p)
    assert "h2" not in json.dumps({k: v for k, v in p.items() if k != "sample_tests"})
    assert "return a + b" not in json.dumps(p)
    assert client.get("/api/problems/none").status_code == 404


def test_problem_list_filters(client):
    ps = client.get("/api/problems", params={"subtopic": "py.a.one"}).json()["problems"]
    assert [p["id"] for p in ps] == ["add-two"]
    assert client.get("/api/problems", params={"difficulty": "hard"}).json()["problems"] == []
    assert client.get("/api/problems", params={"status": "solved"}).json()["problems"] == []
    assert client.get("/api/problems", params={"status": "bogus"}).status_code == 422


def test_subtopic_detail(client):
    s = client.get("/api/subtopics/py.a.one").json()
    assert s["problems"][0]["role"] == "practice"
    assert [(c["level"], c["type"]) for c in s["checks"]] == [
        (1, "concept"),
        (2, "write_code"),
        (3, "write_code"),
    ]
    assert client.get("/api/subtopics/zzz").status_code == 404


def test_hidden_tests_need_a_submit_token(client):
    assert client.get("/api/problems/add-two/tests/hidden").json()["error"]["code"] == (
        "submit_token_required"
    )
    assert client.get("/api/problems/add-two/tests/hidden?token=bad").status_code == 403
    tok = client.post("/api/problems/add-two/start-submit").json()
    r = client.get("/api/problems/add-two/tests/hidden", headers={"X-Submit-Token": tok["token"]})
    assert r.status_code == 200
    assert [t["id"] for t in r.json()["tests"]] == ["h1", "h2"]
    assert r.json()["limits"]["time_ms"] == 1000
    # also accepted as a query parameter
    assert client.get(f"/api/problems/add-two/tests/hidden?token={tok['token']}").status_code == 200


def test_submit_token_expires_after_15_minutes(client, clock):
    tok = client.post("/api/problems/add-two/start-submit").json()["token"]
    clock.advance(minutes=14)
    assert client.get(f"/api/problems/add-two/tests/hidden?token={tok}").status_code == 200
    clock.advance(minutes=2)
    r = client.get(f"/api/problems/add-two/tests/hidden?token={tok}")
    assert r.status_code == 403 and r.json()["error"]["code"] == "submit_token_expired"


def test_drafts_hidden_by_default_and_served_in_dev(tmp_path, settings, clock, draft_content_dir):
    settings.content_dir = draft_content_dir
    rt = Runtime(settings, clock=clock)
    with TestClient(create_app(settings, rt)) as c:
        assert c.get("/api/lessons/py.a.one").status_code == 404
        assert c.get("/api/problems/add-two").status_code == 404
        assert c.get("/api/map").json()["subtopics"][0]["content_status"] == "none"
    settings.serve_drafts = True
    settings.data_dir = tmp_path / "data2"
    rt = Runtime(settings, clock=clock)
    with TestClient(create_app(settings, rt)) as c:
        assert c.get("/api/lessons/py.a.one").status_code == 200
        assert c.get("/api/problems/add-two").status_code == 200
        assert c.get("/api/map").json()["subtopics"][0]["content_status"] == "draft"


def test_real_content_loads(tmp_path):
    store = ContentStore.load(REPO_ROOT / "content", serve_drafts=True)
    assert len(store.subtopics) == 40
    assert "ransom-note" in store.problems
    assert store.hidden_tests(store.problems["ransom-note"])
    s = Settings(
        data_dir=tmp_path / "d",
        content_dir=REPO_ROOT / "content",
        allow_network_fs=True,
        serve_drafts=True,
    )
    with TestClient(create_app(s)) as c:
        assert len(c.get("/api/map").json()["subtopics"]) == 40
        assert c.get("/api/lessons/py.datastructs.dict").status_code == 200
        assert c.get("/api/problems/ransom-note").json()["id"] == "ransom-note"
