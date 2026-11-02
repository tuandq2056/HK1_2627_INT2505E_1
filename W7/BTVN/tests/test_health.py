def test_healthz_does_not_touch_db(client, count_queries):
    with count_queries() as q:
        resp = client.get("/healthz")

    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}
    assert q.count == 0


def test_ready_checks_db(client):
    resp = client.get("/ready")

    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok", "checks": {"db": "ok"}}
