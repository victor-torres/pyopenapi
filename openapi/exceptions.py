import typing


class OpenAPIException(Exception):

    pass


class ValidationError(OpenAPIException):

    def __init__(self, errors: typing.List[str]):
        self.errors = errors


class NotFoundError(OpenAPIException):

    def __init__(self, path: str):
        self.path = path


class MethodNotAllowed(OpenAPIException):

    def __init__(self, path: str, method: str):
        self.path = path
        self.method = method
