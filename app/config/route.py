class Path:
    """
    Helper class to define url rules.
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
    rules(list): a list of class Path objects.
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
