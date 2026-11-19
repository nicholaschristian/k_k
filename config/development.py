from config.base import Config


class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = "DEBUG"
