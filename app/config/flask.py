from flask import Flask
from .csrf import csrf


__all__ = ['Application']


class Application(Flask):
    """
    Base Flask Class
    """
    def __init__(self, *args, **kwargs):
        Flask.__init__(self, *args, **kwargs)

        """Registers csrf protection"""
        csrf.init_app(self)
