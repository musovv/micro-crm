from sqlalchemy import inspect


def break_circular(func):
    """
    Decorator to break circular references
    :param func: the function to decorate
    :return: result of the function
    """
    def wrapper(self, refs=None):
        if refs is None:
            refs = set()
        if id(self) in refs:
            return None
        refs.add(id(self))
        # print(f'DEBUG>> type:{type(self)}, id:{id(self)}; refs: {refs}')
        return func(self, refs)
    return wrapper


def break_circular2(func):
    """
    Decorator to break a circular through counter of deep
    Use to avoid infinite recursion
    :param func: the function to decorate
    :return: result of the function
    """
    def wrapper(self, counter=None):
        if counter is None:
            counter = 0
        if counter >= 3:
            return None
        counter += 1
        return func(self, counter)
    return wrapper


def remove_none(func):
    """
     @deprecated
    :param func:
    :return:
    """
    def inner(self_):
        d = func(self_)
        return {k: v for k, v in d.items() if v is not None}
    return inner
