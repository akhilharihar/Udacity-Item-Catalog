from app.auth.oauth import AbstractOAuth2Provider
from flask import url_for


class GoogleAuth(AbstractOAuth2Provider):
    def __init__(self):
        super().__init__(
                name='google',
                client_id=self.from_env('GOOGLE_CLIENT_ID'),
                client_secret=self.from_env('GOOGLE_CLIENT_SECRET'),
                api_base_url='https://www.googleapis.com',
                access_token_url='https://www.googleapis.com/oauth2/v4/token',
                access_token_params=None,
                authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
                authorize_params={
                    'access_type': 'offline',
                    'include_granted_scopes': 'true'
                },
                client_kwargs={
                    'token_endpoint_auth_method': 'client_secret_basic',
                    'scope': 'profile email',
                },
        )

    @property
    def redirect_uri(self):
        return url_for('authorise_oauth', name='google', _external=True)

    @property
    def user_info(self):
        return self.client.get('oauth2/v2/userinfo').json()

    @property
    def user_email(self):
        data = self.user_info
        return data['email']

    @property
    def user_id(self):
        data = self.user_info
        return data['id']
