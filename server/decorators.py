import logging
from functools import wraps

logger = logging.getLogger('decorators')

def logged(func):
    def wrapper(request, *args, **kwrags):
        logger.debug(f'{func.__name__}: {request}')
        return func(request, *args, **kwargs)
    return wrapper
