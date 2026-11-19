import click
from werkzeug.security import generate_password_hash


def register_cli(app):
    @app.cli.command("hash-password")
    @click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
    def hash_password(password):
        """Print a password hash to paste into ADMIN_PASSWORD_HASH in .env."""
        click.echo(generate_password_hash(password))
