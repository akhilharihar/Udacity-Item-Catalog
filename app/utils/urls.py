from flask import url_for
from werkzeug.urls import url_parse, url_unparse


class Path:
    """
    Helper class to define url rules.
    Params: http://flask.pocoo.org/docs/1.0/api/#flask.Flask.add_url_rule

    Example:
    Path(rule='/', endpoint='index', view_func=index)
    """
    def __init__(self, rule, endpoint, view_func, **kwargs):
        self.__args = kwargs
        self.__args['rule'] = rule
        self.__args['endpoint'] = endpoint
        self.__args['view_func'] = view_func

    @property
    def args(self):
        return self.__args


class Resource:
    """
    Helper class to define url rule with prefix.
    This class removes the need for you to use blueprint to register url rules
    with a prefix.
    params:
    url_prefix(str): string to be prefixed before the url.
    rules(list): a list of class:Path instances.

    Example:
    Resource('admin', [
        Path(rule='/login', endpoint='index', view_func=index)
    ])
    """
    def __init__(self, url_prefix, rules):
        self.__rules = []
        if url_prefix is not None:
            for rule in rules:
                rule.args['rule'] = str(url_prefix) + rule.args['rule']
                self.__rules.append(rule)

    @property
    def urls(self):
        return self.__rules


def url_without_trailing_slash(s, _external=False, **values):
    """
    Generate url for an endpoint without trailing slash.
    """
    ourl = url_for(s, _external=_external, **values)

    ourl_parts = list(url_parse(ourl))

    if ourl_parts[2].endswith('/'):
        ourl_parts[2] = ourl_parts[2][:-1]

    nurl = url_unparse(tuple(ourl_parts))
    return nurl
