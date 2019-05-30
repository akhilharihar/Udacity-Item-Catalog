from flask import Flask


__all__ = ['Application']


class Application(Flask):
    """
    Base Flask Class
    """
    def __init__(self, *args, **kwargs):
        Flask.__init__(self, *args, **kwargs)
