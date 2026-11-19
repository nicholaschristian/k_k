import os

os.environ.setdefault("MONGO_URI", "mongodb://localhost:27017/")
os.environ.setdefault("MONGO_DBNAME", "key_and_kin_test")
os.environ.setdefault("SECRET_KEY", "test-secret")

import pytest
from werkzeug.security import generate_password_hash

from app import create_app
from app.routes import public

ADMIN_EMAIL = "owner@keyandkin.test-fixture"
ADMIN_PASSWORD = "correct horse"


@pytest.fixture()
def app():
    application = create_app("testing")
    application.config["ADMIN_EMAIL"] = ADMIN_EMAIL
    application.config["ADMIN_PASSWORD_HASH"] = generate_password_hash(ADMIN_PASSWORD)
    application.db.inquiries.delete_many({})
    public._recent_submissions.clear()
    yield application


@pytest.fixture()
def db(app):
    return app.db


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def admin_client(client):
    client.post("/admin/login", data={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
    return client
