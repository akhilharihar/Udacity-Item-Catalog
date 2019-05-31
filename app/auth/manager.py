from flask_login import LoginManager


login_manager = LoginManager()

"""Login manager Configuration"""
login_manager.needs_refresh_message = 'Please Login to access this page'
login_manager.login_message_category = "login_info"
