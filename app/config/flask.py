from flask import Flask, Blueprint as BP
from flask.wrappers import Request as Req
from werkzeug.utils import cached_property
from werkzeug.datastructures import MultiDict, CombinedMultiDict
from .csrf import csrf
from .jinja_filters import installed_filters


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


class FlaskHelpers:
    def add_url_rules(self, rules, is_path_instance=True):
        """
        Registers a list of URL rules using flask add_url_rule method.
        params:
        rules(list): A list of path instances.
        is_path_instance(bool): if true, adds url rules from path object or
        directly unpacks the dict object.
        """
        if isinstance(rules, list):
            for rule in rules:
                if is_path_instance:
                    self.add_url_rule(**rule.args)
                else:
                    self.add_url_rule(**rule)
        else:
            raise TypeError('rules must be a list.')


class Application(Flask, FlaskHelpers):
    """
    Base Flask Class
    """

    request_class = Request

    def __init__(self, *args, **kwargs):
        Flask.__init__(self, *args, **kwargs)

        """Registers csrf protection"""
        csrf.init_app(self)

        """Register jinja filters"""
        for filter_name, func in installed_filters.items():
            self.jinja_env.filters[filter_name] = func


class Blueprint(BP, FlaskHelpers):
    """
    Base Flask Blueprint class
    """
    pass
