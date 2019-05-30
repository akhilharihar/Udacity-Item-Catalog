from flask_wtf.csrf import CSRFProtect

__all__ = ['csrf']

csrf = CSRFProtect()  # csrf protection
