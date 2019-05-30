def escape_js_template_tags(s):
    """
    Jinja Filter to escape javascript template variables.
    """
    return '{{' + str(s) + '}}'


installed_filters = {
    'vue': escape_js_template_tags
}
