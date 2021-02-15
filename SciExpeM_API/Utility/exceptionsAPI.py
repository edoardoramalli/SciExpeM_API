class HTTP_SERVER_EXCEPTION(Exception):
    def __init__(self, status_code, *args, **kwargs):
        msg = "Http Status Code " + str(status_code)
        super().__init__(msg, *args, **kwargs)


class HTTP_CLIENT_EXCEPTION(Exception):
    def __init__(self, status_code, *args, **kwargs):
        msg = "Http Status Code " + str(status_code)
        super().__init__(msg, *args, **kwargs)


class HTTP_REDIRECTION_EXCEPTION(Exception):
    def __init__(self, status_code, *args, **kwargs):
        msg = "Http Status Code " + str(status_code)
        super().__init__(msg, *args, **kwargs)


class API_PROCESSING_EXCEPTION(Exception):
    def __init__(self, error, *args, **kwargs):
        msg = "This error occurs during the processing on the server. " + error
        super().__init__(msg, *args, **kwargs)


class API_CONNECTION_EXCEPTION(Exception):
    def __init__(self, error, *args, **kwargs):
        msg = "It is not possible to connect to API server. " + error
        super().__init__(msg, *args, **kwargs)
