import functools

from loguru import logger

from rest_framework.response import Response


def handle_unexpected_exception(func):
    """ Decorator to handle unexpected exceptions in API views """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(e)
            return Response(status=500, data={"message": "Unexpected error occurred"})

    return wrapper
