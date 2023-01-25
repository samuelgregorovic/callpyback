from utils import _callback


def callpyback(on_success, on_fail, on_end):
    def wrapper(func):
        def inner(*func_args, **func_kwargs):
            return _callback(
                func=func,
                on_success=on_success,
                on_fail=on_fail,
                on_end=on_end,
                *func_args,
                **func_kwargs,
            )

        return inner

    return wrapper
