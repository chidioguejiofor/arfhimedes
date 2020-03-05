class ResponseException(Exception):
    def __init__(self, *, message, status_code, errors=None):
        self.message = message
        self.errors = errors if errors else {}
        self.status_code = status_code
        print('Called Here ------')
