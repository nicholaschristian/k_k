from config.base import Config


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    MONGO_DBNAME = "key_and_kin_test"
    SESSION_COOKIE_SECURE = False
    INQUIRY_RATE_LIMIT = 1000
