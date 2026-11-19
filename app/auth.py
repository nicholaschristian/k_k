from flask import current_app
from flask_login import UserMixin
from werkzeug.security import check_password_hash


class AdminUser(UserMixin):
    """The single owner account, configured entirely through env vars."""

    def __init__(self, email):
        self.id = email
        self.email = email

    @classmethod
    def load(cls, user_id):
        email = current_app.config.get("ADMIN_EMAIL")
        if email and user_id == email:
            return cls(email)
        return None

    @classmethod
    def authenticate(cls, email, password):
        expected_email = current_app.config.get("ADMIN_EMAIL")
        password_hash = current_app.config.get("ADMIN_PASSWORD_HASH")
        if not expected_email or not password_hash:
            return None
        if (email or "").strip().lower() != expected_email:
            return None
        if not check_password_hash(password_hash, password or ""):
            return None
        return cls(expected_email)
