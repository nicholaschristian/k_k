from app.services.inquiry_service import InquiryService
from tests.conftest import ADMIN_EMAIL


def _seed(db, **overrides):
    data = {"name": "Sam Lee", "email": "sam@example.com", "event_type": "corporate",
            "guest_count": 40, "location": "Downtown office"}
    data.update(overrides)
    return InquiryService(db).create(data)


def test_admin_requires_login(client):
    resp = client.get("/admin/")
    assert resp.status_code == 302
    assert "/admin/login" in resp.headers["Location"]


def test_wrong_password_rejected(client):
    resp = client.post("/admin/login", data={"email": ADMIN_EMAIL, "password": "nope"})
    assert resp.status_code == 200
    assert "don&#39;t match" in resp.get_data(as_text=True)
    assert client.get("/admin/").status_code == 302


def test_login_disabled_without_hash(app, client):
    app.config["ADMIN_PASSWORD_HASH"] = None
    client.post("/admin/login", data={"email": ADMIN_EMAIL, "password": "anything"})
    assert client.get("/admin/").status_code == 302


def test_open_redirect_blocked(client):
    from tests.conftest import ADMIN_PASSWORD

    resp = client.post("/admin/login?next=https://evil.example/",
                       data={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
    assert resp.headers["Location"].endswith("/admin/")


def test_list_shows_inquiries(admin_client, db):
    _seed(db, name="Sam Lee")
    _seed(db, name="Rin Ito")
    body = admin_client.get("/admin/").get_data(as_text=True)
    assert "Sam Lee" in body and "Rin Ito" in body


def test_status_update_and_filter(admin_client, db):
    doc = _seed(db, name="Sam Lee")
    _seed(db, name="Rin Ito")
    resp = admin_client.post(f"/admin/inquiries/{doc['_id']}/status", data={"status": "booked"})
    assert resp.status_code == 302
    assert db.inquiries.find_one({"_id": doc["_id"]})["status"] == "booked"

    body = admin_client.get("/admin/?status=booked").get_data(as_text=True)
    assert "Sam Lee" in body and "Rin Ito" not in body


def test_status_update_rejects_bad_values(admin_client, db):
    doc = _seed(db)
    assert admin_client.post(f"/admin/inquiries/{doc['_id']}/status", data={"status": "lost"}).status_code == 400
    assert admin_client.post("/admin/inquiries/not-an-id/status", data={"status": "booked"}).status_code == 404


def test_logout(admin_client):
    admin_client.post("/admin/logout")
    assert admin_client.get("/admin/").status_code == 302
