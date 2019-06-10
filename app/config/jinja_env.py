from app.utils import url

__all__ = ['installed_filters', 'installed_tags']


def escape_js_template_tags(s):
    """
    Jinja Filter to escape javascript template variables.
    """
    return '{{' + str(s) + '}}'


installed_filters = {
    'vue': escape_js_template_tags
}

installed_tags = {
    'url': url
}
