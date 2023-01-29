import sys
import inspect
import asyncio

# default callback functions
DEFAULT_ON_CALL_LAMBDA = lambda *a, **k: None
DEFAULT_ON_SUCCESS_LAMBDA = lambda *a, **k: None
DEFAULT_ON_FAILURE_LAMBDA = lambda *a, **l: None
DEFAULT_ON_END_LAMBDA = lambda *a, **k: None


class CallPyBack:
    # decorator init
    def __init__(
        self,
        on_call=DEFAULT_ON_CALL_LAMBDA,
        on_success=DEFAULT_ON_SUCCESS_LAMBDA,
        on_failure=DEFAULT_ON_FAILURE_LAMBDA,
        on_end=DEFAULT_ON_END_LAMBDA,
        default_return=None,
        pass_vars=None,
    ):
        self.on_call = on_call
        self.on_success = on_success
        self.on_failure = on_failure
        self.on_end = on_end
        self.default_return = default_return
        self.pass_vars = pass_vars
        self.local_vars = {}

    def __call__(self, func):
        # call of the decorated function
        def tracer(frame, event, arg):
            # setup for pulling locals
            if event == "return":
                self.local_vars = frame.f_locals.copy()

        def wrapper(*func_args, **func_kwargs):
            # callback and func flow
            sys.setprofile(tracer)
            func_exception, func_result, func_scope_vars = None, None, []
            try:
                self.run_on_call_func(func_args, func_kwargs)
                func_result = func(*func_args, **func_kwargs)
                func_scope_vars = self.get_func_scope_vars()
                self.run_success_func(func_result, func_args, func_kwargs)
                return func_result
            except Exception as ex:
                func_exception = ex
                func_scope_vars = self.get_func_scope_vars()
                self.run_failure_func(func_exception, func_args, func_kwargs)
                return self.default_return
            finally:
                sys.setprofile(None)
                if self.is_on_end_func_defined():
                    raise func_exception
                result = func_result if not func_exception else self.default_return
                self.run_on_end_func(
                    result, func_exception, func_args, func_kwargs, func_scope_vars
                )
                return result

        return wrapper

    ############### CALLING CALLBACKS ###############

    def run_callback_func(self, func, func_kwargs):
        # generalised call to given callback func
        if inspect.iscoroutinefunction(self.on_call):
            asyncio.run(func(**func_kwargs))
        else:
            func(func_kwargs)

    def run_on_call_func(self, func_args, func_kwargs):
        on_call_kwargs = self.get_on_call_kwargs(func_args, func_kwargs)
        self.run_callback_func(self.on_call, on_call_kwargs)

    def run_success_func(self, func_result, func_args, func_kwargs):
        on_success_kwargs = self.get_on_success_kwargs(
            func_result, func_args, func_kwargs
        )
        self.run_callback_func(self.on_success, on_success_kwargs)

    def run_failure_func(self, func_exception, func_args, func_kwargs):
        on_failure_kwargs = self.get_on_failure_kwargs(
            func_exception, func_args, func_kwargs
        )
        self.run_callback_func(self.on_failure, on_failure_kwargs)

    def run_on_end_func(
        self, func_result, func_exception, func_args, func_kwargs, func_scope_vars
    ):
        on_end_kwargs = self.get_on_end_kwargs(
            func_result, func_exception, func_args, func_kwargs, func_scope_vars
        )
        self.run_callback_func(self.on_end, on_end_kwargs)

    ############### END CALLING CALLBACKS ###############

    def get_func_scope_vars(self):
        # getting local variables from func scope based on pass_vars param
        func_scope_vars = {}
        if not self.pass_vars:
            return []
        for var_name in self.pass_vars:
            func_scope_vars[var_name] = self.local_vars.get(var_name, "<not-found>")
        self.local_vars = {}
        return func_scope_vars

    def is_on_end_func_defined(self):
        # check if on_end handling function is defined
        return (
            isinstance(self.on_end, type(DEFAULT_ON_END_LAMBDA))
            and self.on_end.__name__ == DEFAULT_ON_END_LAMBDA.__name__
            and self.on_end == DEFAULT_ON_END_LAMBDA
        )

    ############### CONSTRUCTING KWARGS FOR CALLBACKS ###############
    # to allow omitting parameters in user created callbacks

    def get_on_call_kwargs(self, func_args, func_kwargs):
        # constructing on_call kwargs
        kwargs = {}
        params = inspect.signature(self.on_success).parameters
        if "func_args" in params:
            kwargs["func_args"] = func_args
        if "func_kwargs" in params:
            kwargs["func_kwargs"] = func_kwargs
        return kwargs

    def get_on_success_kwargs(self, func_result, func_args, func_kwargs):
        # constructing on_success kwargs
        kwargs = {}
        params = inspect.signature(self.on_success).parameters
        if "func_result" in params:
            kwargs["func_result"] = func_result
        if "func_args" in params:
            kwargs["func_args"] = func_args
        if "func_kwargs" in params:
            kwargs["func_kwargs"] = func_kwargs
        return kwargs

    def get_on_failure_kwargs(self, func_exception, func_args, func_kwargs):
        # constructing on_failure kwargs
        kwargs = {}
        params = inspect.signature(self.on_failure).parameters
        if "func_exception" in params:
            kwargs["func_exception"] = func_exception
        if "func_args" in params:
            kwargs["func_args"] = func_args
        if "func_kwargs" in params:
            kwargs["func_kwargs"] = func_kwargs
        return kwargs

    def get_on_end_kwargs(
        self, func_result, func_exception, func_args, func_kwargs, func_scope_vars
    ):
        # constructing on_end kwargs
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
        if "func_scope_vars" in params:
            kwargs["func_scope_vars"] = func_scope_vars
        return kwargs
