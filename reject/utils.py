import types


def is_savable(var):
    if isinstance(var, types.LambdaType):
        return False
    return True
