from flask import Flask
from flask.wrappers import Request as Req
from werkzeug.utils import cached_property
from werkzeug.datastructures import MultiDict, CombinedMultiDict
from .csrf import csrf


__all__ = ['Application']


class Request(Req):
    """
    Extends Flask Request class.
    """
    @cached_property
    def input_values(self):
        """Combines :attr:`json` and :attr:`form` to a
        `werkzeug.datastructures.CombinedMultiDict` object."""
        args = []
        for d in self.form, self.json:
            if not isinstance(d, MultiDict):
                d = MultiDict(d)
            args.append(d)
        return CombinedMultiDict(args)


class Application(Flask):
    """
    Base Flask Class
    """

    request_class = Request

    def __init__(self, *args, **kwargs):
        Flask.__init__(self, *args, **kwargs)

        """Registers csrf protection"""
        csrf.init_app(self)
