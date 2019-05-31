from .manager import login_manager
from .oauth_providers.google import GoogleAuth

installed_auth_providers = {
    'google': GoogleAuth
}

__all__ = ['login_manager',  'installed_auth_providers']
