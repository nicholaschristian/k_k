from config.base import Config


class ProductionConfig(Config):
    DEBUG = False
    # TRUST_PROXY_HEADERS / SESSION_COOKIE_SECURE stay env-driven (see base.py):
    # forcing them on here breaks admin login over plain HTTP on the LAN.
