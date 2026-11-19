from flask_login import LoginManager
from flask_wtf import CSRFProtect

login_manager = LoginManager()
login_manager.login_view = "admin.login"
login_manager.login_message = "Log in to view inquiries."
login_manager.login_message_category = "info"

csrf = CSRFProtect()
