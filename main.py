def _callback(func, on_success, on_fail, on_end, *func_args, **func_kwargs):
    try:
        func_result = func(*func_args, **func_kwargs)
        on_success()
        return func_result
    except Exception as ex:
        on_fail(ex)
    finally:
        on_end()


def pyback(on_success, on_fail, on_end):
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


class PyBack:
    def __init__(self, on_success, on_fail, on_end):
        self.on_success = on_success
        self.on_fail = on_fail
        self.on_end = on_end

    def __call__(self, func):
        def wrapper(*func_args, **func_kwargs):
            return _callback(
                func=func,
                on_success=self.on_success,
                on_fail=self.on_fail,
                on_end=self.on_end,
                *func_args,
                **func_kwargs,
            )

        return wrapper
