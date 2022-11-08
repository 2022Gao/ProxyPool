class PoolEmptyError(Exception):
    """
    Raise an exception
    when the proxy pool is empty.
    """

    def __init__(self):
        super().__init__()

    def __str__(self):
        return repr('The proxy source is exhausted.')


class ResourceDepletionError(Exception):
    """
    Raise an exception when the proxy
    is not available for a long time.
    """

    def __init__(self):
        super().__init__()

    def __str__(self):
        return repr('There are not more proxies in internet.')


class RewriteSpiderError(Exception):
    """
    Raise an exception when the
    new spider class didn't follow
    the format of spider metaclass.
    """

    def __init__(self, cls_name):
        self.cls_name = cls_name
        super().__init__()

    def __str__(self):
        return repr(f'The spider `{self.cls_name}` does not has func `gets`.')


if __name__ == '__main__':
    raise ResourceDepletionError