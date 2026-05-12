from fastapi.testclient import TestClient

import app

client = TestClient(app.app)


def setup_function():
    app.reset_state()


def test_health():
    resp = client.get('/health')
    assert resp.status_code == 200
    assert resp.json()['status'] == 'ok'


def test_join_and_list_queue():
    r1 = client.post('/queue/join', json={'phone': '+525511223344'})
    assert r1.status_code == 200
    assert r1.json()['ticket'] == 1

    r2 = client.get('/queue')
    assert r2.status_code == 200
    body = r2.json()
    assert body['now_serving'] is None
    assert len(body['waiting']) == 1


def test_prevent_duplicate_waiting_phone():
    client.post('/queue/join', json={'phone': '+525511223344'})
    dup = client.post('/queue/join', json={'phone': '+525511223344'})
    assert dup.status_code == 409


def test_advance_marks_serving_and_done():
    client.post('/queue/join', json={'phone': '+11111111111'})
    client.post('/queue/join', json={'phone': '+22222222222'})

    first = client.post('/queue/advance', json={'count': 1})
    assert first.status_code == 200
    assert first.json()['now_serving'] == 1
    assert len(first.json()['waiting']) == 1

    second = client.post('/queue/advance', json={'count': 1})
    assert second.status_code == 200
    assert second.json()['now_serving'] == 2
