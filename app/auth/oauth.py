from authlib.flask.client import OAuth
from abc import ABC, abstractmethod
import os

oauth = OAuth()


class AbstractOAuth2Provider(ABC):
    """
    Abstract Class to implement an oauth provider.
    """
    def __init__(self, **kwargs):
        self.__client = oauth.register(**kwargs)

    @property
    def client(self):
        """
        Get oauth client
        """
        return self.__client

    @property
    @abstractmethod
    def redirect_uri(self):
        """
        application url to handle oAuth authorisation response.
        """
        pass

    def from_env(self, key):
        """
        Helper method to get values from env.
        """
        return os.getenv(key)

    def set_token(self, token):
        """
        set user token to perform operations with the oauth provider.
        """
        self.client._fetch_token = token

    @property
    @abstractmethod
    def user_email(self):
        """
        get user email address.
        """
        pass

    @property
    @abstractmethod
    def user_id(self):
        """
        Get user id from oauth provider.
        """
        pass
