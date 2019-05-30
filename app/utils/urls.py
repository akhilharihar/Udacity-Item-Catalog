class Path:
    """
    Helper class to define url rules.
    """
    def __init__(self, **kwargs):
        self.__args = kwargs

    @property
    def args(self):
        return self.__args
