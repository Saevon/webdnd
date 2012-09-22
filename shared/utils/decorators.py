from functools import wraps

def cascade(func):
    """
    class method decorator, always returns the
    object that called the method
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        return self
    return wrapper
