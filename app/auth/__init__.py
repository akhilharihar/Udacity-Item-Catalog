from .manager import login_manager
from .oauth_providers.google import GoogleAuth
from .oauth_providers.facebook import FacebookAuth

auth_providers = {
    'google': GoogleAuth,
    'facebook': FacebookAuth
}

__all__ = ['login_manager',  'auth_providers']
