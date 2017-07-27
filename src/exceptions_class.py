class Error(Exception):
    """
    Base class for other exceptions
    """
    pass


class EventDoesNotExist(Error):
    """
    Raised when the event does not exist
    """
    def __init__(self, type, key):
        self.msg = '{0} event with key id : {1} does not exist to UPDATE'.format(type, key)


class UndefinedVerb(Error):
    """
    Raised when the event does not exist
    """
    def __init__(self, verb, type, key):
        self.msg = 'verb : {0} undefined for {1} event with key id : {1}'.format(verb, type, key)



