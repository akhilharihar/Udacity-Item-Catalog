from authlib.flask.client import OAuth
from abc import ABC, abstractmethod
import os

oauth = OAuth()


class AbstractOAuth2Provider(ABC):
    def __init__(self, **kwargs):
        self.__client = oauth.register(**kwargs)

    @property
    def client(self):
        return self.__client

    @property
    @abstractmethod
    def redirect_uri(self):
        pass

    def from_env(self, key):
        return os.getenv(key)

    def set_token(self, token):
        self.client._fetch_token = token

    @property
    @abstractmethod
    def user_email(self):
        pass

    @property
    @abstractmethod
    def user_id(self):
        pass
