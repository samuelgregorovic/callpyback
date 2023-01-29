import inspect
import asyncio


class CallPyBack:
    def __init__(
        self,
        on_success=lambda *a, **k: None,
        on_failure=lambda *a, **k: None,
        on_end=lambda *a, **k: None,
        default_return=None,
    ):
        self.on_success = on_success
        self.on_failure = on_failure
        self.on_end = on_end
        self.default_return = default_return

    def __call__(self, func):
        def wrapper(*func_args, **func_kwargs):
            try:
                func_exception, func_result = None, None
                func_result = func(*func_args, **func_kwargs)
                success_kwargs = self.get_success_kwargs(
                    func_result, func_args, func_kwargs
                )
                if inspect.iscoroutinefunction(self.on_success):
                    asyncio.run(self.on_success(**success_kwargs))
                else:
                    self.on_success(**success_kwargs)
                return func_result
            except Exception as ex:
                func_exception = ex
                func_result = None
                failure_kwargs = self.get_failure_kwargs(
                    func_exception, func_args, func_kwargs
                )
                if inspect.iscoroutinefunction(self.on_failure):
                    asyncio.run(self.on_failure(**failure_kwargs))
                else:
                    self.on_failure(**failure_kwargs)
                return self.default_return
            finally:
                on_end_kwargs = self.get_on_end_kwargs(
                    func_result, func_exception, func_args, func_kwargs
                )
                if inspect.iscoroutinefunction(self.on_end):
                    asyncio.run(self.on_end(**on_end_kwargs))
                else:
                    self.on_end(**on_end_kwargs)
                return self.default_return

        return wrapper

    def get_success_kwargs(self, func_result, func_args, func_kwargs):
        kwargs = {}
        params = inspect.signature(self.on_success).parameters
        if "func_result" in params:
            kwargs["func_result"] = func_result
        if "func_args" in params:
            kwargs["func_args"] = func_args
        if "func_kwargs" in params:
            kwargs["func_kwargs"] = func_kwargs
        return kwargs

    def get_failure_kwargs(self, func_exception, func_args, func_kwargs):
        kwargs = {}
        params = inspect.signature(self.on_failure).parameters
        if "func_exception" in params:
            kwargs["func_exception"] = func_exception
        if "func_args" in params:
            kwargs["func_args"] = func_args
        if "func_kwargs" in params:
            kwargs["func_kwargs"] = func_kwargs
        return kwargs

    def get_on_end_kwargs(self, func_result, func_exception, func_args, func_kwargs):
        kwargs = {}
        params = inspect.signature(self.on_end).parameters
        if "func_result" in params:
            kwargs["func_result"] = func_result
        if "func_exception" in params:
            kwargs["func_exception"] = func_exception
        if "func_args" in params:
            kwargs["func_args"] = func_args
        if "func_kwargs" in params:
            kwargs["func_kwargs"] = func_kwargs
        return kwargs
