import functools
import inspect


def rule(code, message):
    def wrapper(func):
        func.code = code
        func.message = message
        return func
    return wrapper


def rule_factory(code, message):
    def wrapper(func: callable):

        signature = inspect.signature(func)

        @functools.wraps(func)
        def inner_wrapper(*args, **kwargs):
            bound = signature.bind(*args, **kwargs)
            bound.apply_defaults()
            validator = func(*args, **kwargs)
            validator.code = code
            validator.params = dict(bound.arguments)
            validator.message = message.format(**bound.arguments)
            
            return validator

        return inner_wrapper
    return wrapper
