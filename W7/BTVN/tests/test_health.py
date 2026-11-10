def test_healthz_does_not_touch_db(client, queries):
    resp = client.get("/healthz")

    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}
    assert len(queries) == 0


def test_ready_checks_db(client, queries):
    resp = client.get("/ready")

    assert resp.status_code == 200
    assert resp.get_json()["db"] == "ok"
    assert len(queries) == 1
