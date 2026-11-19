import os


def _env_bool(name, default=False):
    return os.environ.get(name, str(default)).strip().lower() in ("1", "true", "yes", "on")


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-not-for-production")

    MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
    MONGO_DBNAME = os.environ.get("MONGO_DBNAME", "key_and_kin")

    # Unique cookie name so this app never collides with another Shao Box app's
    # "session" cookie if they end up behind the same reverse-proxy domain.
    SESSION_COOKIE_NAME = "kk_session"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    # Default False: reached over plain HTTP on the LAN today. A Secure cookie is
    # silently dropped over HTTP, which breaks admin login. Flip once behind TLS.
    SESSION_COOKIE_SECURE = _env_bool("SESSION_COOKIE_SECURE", False)
    TRUST_PROXY_HEADERS = _env_bool("TRUST_PROXY_HEADERS", False)

    WTF_CSRF_ENABLED = True
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

    # Single admin login, read from env. Generate the hash with `flask hash-password`.
    ADMIN_EMAIL = (os.environ.get("ADMIN_EMAIL") or "").strip().lower() or None
    ADMIN_PASSWORD_HASH = os.environ.get("ADMIN_PASSWORD_HASH") or None

    # Inquiry submissions allowed per client IP per hour (in-memory, per worker).
    INQUIRY_RATE_LIMIT = int(os.environ.get("INQUIRY_RATE_LIMIT", "5"))
