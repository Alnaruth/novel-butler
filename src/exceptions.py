class UnsupportedBrowserException(Exception):
    pass
class NoResultsSearchException(Exception):
    def __init__(self, message=''):
        super(NoResultsSearchException, self).__init__(message)
