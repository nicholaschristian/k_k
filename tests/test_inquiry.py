from datetime import date, timedelta


def valid_data(**overrides):
    data = {
        "name": "Ada Park",
        "email": "ada@example.com",
        "phone": "555-0100",
        "event_date": (date.today() + timedelta(days=60)).isoformat(),
        "event_type": "wedding",
        "guest_count": "120",
        "location": "Riverside Barn",
        "package": "celebration",
        "notes": "Oat milk heavy crowd.",
    }
    data.update(overrides)
    return data


def test_home_renders_sections(client):
    resp = client.get("/")
    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    for anchor in ('id="how"', 'id="menu"', 'id="packages"', 'id="faq"', 'id="inquire"'):
        assert anchor in body
    assert "Honey lavender latte" in body


def test_healthz(client):
    assert client.get("/healthz").get_json() == {"status": "ok"}


def test_valid_inquiry_is_saved(client, db):
    resp = client.post("/inquire", data=valid_data())
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/thanks")
    doc = db.inquiries.find_one()
    assert doc["name"] == "Ada Park"
    assert doc["guest_count"] == 120
    assert doc["status"] == "new"
    assert doc["event_date"].date() == date.today() + timedelta(days=60)
    assert "website" not in doc


def test_invalid_email_rejected(client, db):
    resp = client.post("/inquire", data=valid_data(email="not-an-email"))
    assert resp.status_code == 400
    assert "Enter a valid email address" in resp.get_data(as_text=True)
    assert db.inquiries.count_documents({}) == 0


def test_past_date_rejected(client, db):
    resp = client.post("/inquire", data=valid_data(event_date="2020-01-01"))
    assert resp.status_code == 400
    assert "hasn&#39;t passed yet" in resp.get_data(as_text=True)
    assert db.inquiries.count_documents({}) == 0


def test_missing_required_fields_keep_entered_values(client, db):
    resp = client.post("/inquire", data=valid_data(location="", guest_count=""))
    body = resp.get_data(as_text=True)
    assert resp.status_code == 400
    assert "Enter the venue or city." in body
    assert "Enter a rough guest count." in body
    assert 'value="Ada Park"' in body
    assert db.inquiries.count_documents({}) == 0


def test_honeypot_drops_submission(client, db):
    resp = client.post("/inquire", data=valid_data(website="http://spam.example"))
    assert resp.status_code == 302
    assert db.inquiries.count_documents({}) == 0


def test_rate_limit(app, client, db):
    app.config["INQUIRY_RATE_LIMIT"] = 2
    for _ in range(2):
        assert client.post("/inquire", data=valid_data()).status_code == 302
    resp = client.post("/inquire", data=valid_data())
    assert resp.status_code == 429
    assert db.inquiries.count_documents({}) == 2


def test_csrf_enforced_when_enabled(app, client, db):
    app.config["WTF_CSRF_ENABLED"] = True
    resp = client.post("/inquire", data=valid_data())
    assert resp.status_code == 400
    assert db.inquiries.count_documents({}) == 0
