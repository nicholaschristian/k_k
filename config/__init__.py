import os

from config.development import DevelopmentConfig
from config.production import ProductionConfig
from config.testing import TestingConfig

_CONFIGS = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


def get_config(env_name=None):
    name = env_name or os.environ.get("FLASK_ENV", "production")
    return _CONFIGS.get(name, ProductionConfig)
