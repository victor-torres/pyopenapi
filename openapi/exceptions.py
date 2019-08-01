import typing


class OpenAPIException(Exception):

    pass


class ValidationError(OpenAPIException):

    def __init__(self, errors: typing.List[str]):
        self.errors = errors


class NotFoundError(OpenAPIException):

    pass
