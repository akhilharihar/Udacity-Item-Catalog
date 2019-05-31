from app.auth.oauth import AbstractOAuth2Provider
from flask import url_for


class FacebookAuth(AbstractOAuth2Provider):
    def __init__(self):
        token_url = 'https://graph.facebook.com/v3.3/oauth/access_token'
        super().__init__(
                name='facebook',
                client_id=self.from_env('FACEBOOK_CLIENT_ID'),
                client_secret=self.from_env('FACEBOOK_CLIENT_SECRET'),
                api_base_url='https://graph.facebook.com/v3.3',
                access_token_url=token_url,
                authorize_url='https://www.facebook.com/v3.3/dialog/oauth',
                client_kwargs={
                    'token_endpoint_auth_method': 'client_secret_basic',
                    'scope': 'email public_profile',
                },
        )

    @property
    def redirect_uri(self):
        return url_for('authorise_oauth', name='facebook', _external=True)

    @property
    def user_email(self):
        data = self.client.get('me?fields=email').json()
        return data['email']

    @property
    def user_id(self):
        data = self.client.get('me?fields=id').json()
        return data['id']
