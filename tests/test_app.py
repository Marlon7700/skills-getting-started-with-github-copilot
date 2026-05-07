import src.app as app_module
from urllib.parse import quote
import uuid


def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data


def test_signup_and_remove(client):
    activity = "Chess Club"
    quoted = quote(activity, safe="")
    email = f"test+{uuid.uuid4().hex}@example.com"

    signup_resp = client.post(f"/activities/{quoted}/signup", params={"email": email})
    assert signup_resp.status_code == 200

    data = client.get("/activities").json()
    assert email in data[activity]["participants"]

    delete_resp = client.delete(f"/activities/{quoted}/participants", params={"email": email})
    assert delete_resp.status_code == 200

    data2 = client.get("/activities").json()
    assert email not in data2[activity]["participants"]


def test_signup_duplicate(client):
    activity = "Chess Club"
    quoted = quote(activity, safe="")
    email = f"dup+{uuid.uuid4().hex}@example.com"

    first = client.post(f"/activities/{quoted}/signup", params={"email": email})
    assert first.status_code == 200

    second = client.post(f"/activities/{quoted}/signup", params={"email": email})
    assert second.status_code == 400
