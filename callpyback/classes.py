from utils import _callback


class CallPyBack:
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
