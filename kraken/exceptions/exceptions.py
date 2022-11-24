class KrakenExceptions(object):

    class MaxReconnectError(Exception):
        '''Raised when websocket connection has to many reconnects'''
        def __init__(self, message=''):
            super(Exception, self).__init__(message)

    class KrakenAuthenticationError(Exception):
        '''Raised when credentials are invalid/kraken responses "authenticationError"'''
        def __init__(self, message=''):
            super(Exception, self).__init__(message)

    class KrakenPermissionDeniedError(Exception):
        '''Raised when credentials are valid but permissions are restricted'''
        def __init__(self, message=''):
            super(Exception, self).__init__(message)
    class KrakenServiceUnavailableError(Exception):
        '''Raised when service is unavailable'''
        def __init__(self, message=''):
            super(Exception, self).__init__(message)