from flask import url_for
from werkzeug.urls import url_parse, url_unparse

__all__ = ['installed_filters', 'installed_tags']


def escape_js_template_tags(s):
    """
    Jinja Filter to escape javascript template variables.
    """
    return '{{' + str(s) + '}}'


def url_without_trailing_slash(s, _external=False, **values):
    ourl = url_for(s, _external=False, **values)

    ourl_parts = list(url_parse(ourl))

    if ourl_parts[2].endswith('/'):
        ourl_parts[2] = ourl_parts[2][:-1]

    nurl = url_unparse(tuple(ourl_parts))
    return nurl


installed_filters = {
    'vue': escape_js_template_tags
}

installed_tags = {
    'url': url_without_trailing_slash
}
