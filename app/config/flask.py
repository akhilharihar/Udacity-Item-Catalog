from flask import Flask, Blueprint as BP, request, redirect
from flask.wrappers import Request as Req
from werkzeug.utils import cached_property
from werkzeug.datastructures import MultiDict, CombinedMultiDict
from .csrf import csrf
from .jinja_env import installed_filters, installed_tags
from .errors import http_error_status_codes, BaseError, url_404, url_503
from app.utils import Path, Resource


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
    def add_url_rules(self, rules):
        """
        Registers a list of URL rules using flask add_url_rule method.
        params:
        rules(list): A list of class Path or class Resource objects or
        instances.
        """
        url_rules = []

        if not isinstance(rules, list):
            raise TypeError('rules must be a list.')

        for rule in rules:
            if isinstance(rule, Resource):
                for x in rule.urls:
                    url_rules.append(x)
            elif isinstance(rule, Path):
                url_rules.append(rule)
            else:
                raise TypeError('The contents of rules should either be an \
                    instance of Path or Resouce.')

        for rule in url_rules:
            self.add_url_rule(**rule.args)


def _modify_trailing_slash():
    """
    Redirect url with trailing slash to non trailing ones.
    """
    rp = request.path
    qs = request.query_string
    if rp != '/' and rp.endswith('/'):
        return redirect(rp[:-1] + '?' + str(qs, 'utf-8'))


class Application(Flask, FlaskHelpers):
    """
    Base Flask Class
    """

    request_class = Request

    def __init__(self, *args, **kwargs):
        Flask.__init__(self, *args, **kwargs)

        """Registers csrf protection"""
        csrf.init_app(self)

        self.url_map.strict_slashes = False

        self.before_request_funcs[None] = []

        self.before_request_funcs[None].append(_modify_trailing_slash)

        """Jinja configuration"""
        for filter_name, func in installed_filters.items():
            self.jinja_env.filters[filter_name] = func

        for tag_name, func in installed_tags.items():
            self.jinja_env.globals[tag_name] = func

        """Register custom error handlers for flask application."""
        error_fn = BaseError()
        for error_code in http_error_status_codes:
            self.register_error_handler(error_code, error_fn)

        self.add_url_rule('/404', '404', url_404)
        self.add_url_rule('/504', '503', url_503)


class Blueprint(BP, FlaskHelpers):
    """
    Base Flask Blueprint class
    """
    pass
