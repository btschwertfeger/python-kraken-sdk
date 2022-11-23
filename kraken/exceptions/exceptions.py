class KrakenExceptions(object):
    """
    Collector class of Unique Exceptions
    """

    class MaxReconnectError(Exception):
        """
        Exception is inherited from 'BaseException'.
        """
        def __init__(self, message=''):
            # Call the base class constructor with the parameters it needs
            super(Exception, self).__init__(message)