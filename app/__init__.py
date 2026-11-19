import logging
from datetime import datetime, timezone

from flask import Flask, render_template
from werkzeug.middleware.proxy_fix import ProxyFix

from app.db import init_db
from app.extensions import csrf, login_manager
from config import get_config


def create_app(env_name=None, db=None):
    app = Flask(__name__)
    app.config.from_object(get_config(env_name))

    if app.config.get("TRUST_PROXY_HEADERS"):
        app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1, x_for=1)

    _configure_logging(app)

    if db is not None:
        app.db = db
    else:
        init_db(app)

    login_manager.init_app(app)
    csrf.init_app(app)

    _register_user_loader()
    _register_blueprints(app)
    _register_error_handlers(app)
    _register_cli(app)
    _register_context_processors(app)

    @app.route("/healthz")
    def healthz():
        return {"status": "ok"}

    app.logger.info("Key & Kin startup complete (env=%s)", env_name or "production")
    return app


def _configure_logging(app):
    level = getattr(logging, app.config.get("LOG_LEVEL", "INFO"), logging.INFO)
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s [%(name)s] %(message)s")


def _register_user_loader():
    from app.auth import AdminUser

    @login_manager.user_loader
    def load_user(user_id):
        return AdminUser.load(user_id)


def _register_blueprints(app):
    from app.routes.admin import bp as admin_bp
    from app.routes.public import bp as public_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)


def _register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(_error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(error):
        app.logger.exception("Unhandled exception: %s", error)
        return render_template("errors/500.html"), 500


def _register_cli(app):
    from app.cli import register_cli

    register_cli(app)


def _register_context_processors(app):
    from app.content import BRAND

    @app.context_processor
    def inject_globals():
        return {"current_year": datetime.now(timezone.utc).year, "brand": BRAND}
