"""Module containing CallPyBack implementation"""
import sys
import inspect
import threading


def background_callpyback(func):
    """Decorator to mark a callback function as a background task.
    Marking is done by assigning an attribute `background_callpyback` to the decorated function.
    This will cause the callback to be executed in a separate thread without blocking.

    Args:
        func (Callable): Decorated function to be marked as a background task.

    Returns:
        Callable: Decorated function marked as a background task.
    Raises:
        N/A
    """
    func.__background_callpyback__ = True
    return func


def _default_callback(*_, **__):
    """Default callback function to be used when callback function is not provided."""


class CallPyBack:
    """Class implementing callback decorator.

    Attributes:
        N/A

    Methods:
        validate_arguments():
            Runs validation functions for constructor arguments.
        validate_callbacks():
            Validates callbacks passed to class constructor.
        validate_pass_vars():
            Validates `pass_vars` constructor argument.
        validate_exception_classes():
            Validates `exception_classes` constructor argument.
        __call__(func):
            Invoked on decorator instance call.
        tracer(frame, event, _):
            Represents tracer for storing local variables from last executed function.
        run_callback_func(func, func_kwargs):
            Executes given callback function with given kwargs.
        run_on_call_func(func_args, func_kwargs):
            Generates kwargs for given `on_call` callback function and executes
            it with generated kwargs.
        run_on_success_func(func_result, func_args, func_kwargs):
            Generates kwargs for given `on_success` callback function and executes
            it with generated kwargs.
        run_on_failure_func(func_exception, func_args, func_kwargs):
            Generates kwargs for given `on_failure` callback function and executes
            it with generated kwargs.
        run_on_end_func(func_result, func_exception, func_args, func_kwargs, func_scope_vars):
            Generates kwargs for given `on_end` callback function and executes
            it with generated kwargs.
        get_func_scope_vars():
            Gets requested decorated function's scope variables, specified in `pass_vars` attribute.
        get_on_call_kwargs(func_args, func_kwargs):
            Generates kwargs for `on_call` callback function.
        get_on_success_kwargs(func_result, func_args, func_kwargs):
            Generates kwargs for `on_success` callback function.
        get_on_failure_kwargs(func_exception, func_args, func_kwargs):
            Generates kwargs for `on_failure` callback function.
        get_on_end_kwargs(func_result, func_exception, func_args, func_kwargs, func_scope_vars):
            Generates kwargs for `on_end` callback function.
    """

    def __init__(
        self,
        on_call=_default_callback,
        on_success=_default_callback,
        on_failure=_default_callback,
        on_end=_default_callback,
        default_return=None,
        pass_vars=None,
        exception_classes=(Exception,),
    ):
        """Class constructor. Sets instance variables.

        Args:
            on_call (Callable, optional): Function to be called before function execution.
                Defaults to DEFAULT_ON_CALL_LAMBDA.
            on_success (Callable, optional): Function to be called after successfull execution.
                Defaults to DEFAULT_ON_SUCCESS_LAMBDA.
            on_failure (Callable, optional): Function to be called after execution with errors.
                Defaults to DEFAULT_ON_FAILURE_LAMBDA.
            on_end (Callable, optional): Function to be called after execution regardless of result.
                Defaults to DEFAULT_ON_END_LAMBDA.
            default_return (Any, optional): Result to be returned in case of error or no return.
                Defaults to None.
            pass_vars (list|tuple|set, optional): Variable names to be passed to `on_end` callback.
                Defaults to None.
            exception_classes (list|tuple|set): Exception classes to be caught.
                Defaults to (Exception,).

        Returns:
            CallPyBack: decorator instance
        Raises:
            N/A
        """
        self.on_call = on_call
        self.on_success = on_success
        self.on_failure = on_failure
        self.on_end = on_end
        self.default_return = default_return
        self.pass_vars = pass_vars
        self.exception_classes = exception_classes
        self.local_vars = {}
        self.callbacks = (self.on_call, self.on_success, self.on_failure, self.on_end)

    def validate_arguments(self):
        """Runs validation functions for constructor arguments.

        Args:
            None
        Returns:
            N/A
        """
        self.validate_callbacks()
        self.validate_pass_vars()
        self.validate_exception_classes()

    def validate_callbacks(self):
        """Validates callbacks passed to class constructor.

        Executes following checks:
            1. Callback must be a Callable type.
            2. Callback cannot be an async coroutine.

        Args:
            N/A
        Returns:
            None
        Raises:
            TypeError: Raised if one of the callbacks is not Callable.
            TypeError: Raised if one of the callbacks is an async coroutine.
        """
        for callback in self.callbacks:
            if not callable(callback):
                raise TypeError(f"Callback must be a callable not {type(callback)}.")
            if inspect.iscoroutinefunction(callback):
                raise TypeError(
                    f"Callback `{callback.__name__}` cannot be a coroutine."
                )

    def validate_pass_vars(self):
        """Validates `pass_vars` constructor argument.

        Executes following checks:
            1. If `pass_vars` is defined, `on_end` must be defined.
            2. Parameter `pass_vars` must be `list`, `tuple` or `set`.
            3. Variable in `pass_vars` must be of type `str`.

        Args:
            N/A
        Returns:
            None
        Raises:
            RuntimeError: Raised if `pass_vars` is defined but `on_end` callback is not.
            TypeError: Raised if `pass_vars` is not of type `list`, `tuple` or `set`.
            TypeError: Raised if one of variables in `pass_vars` is not of type `str`.
        """
        if not self.pass_vars:
            return
        if self.pass_vars and self.on_end is _default_callback:
            raise RuntimeError("If `pass_vars` is defined, `on_end` must be defined.")
        if not isinstance(self.pass_vars, (list, tuple, set)):
            raise TypeError("Parameter `pass_vars` must be `list`, `tuple` or `set`.")
        for var in self.pass_vars:
            if not isinstance(var, str):
                raise TypeError("Variable in `pass_vars` must be of type `str`.")

    def validate_exception_classes(self):
        """Validates `exception_classes` constructor argument.

        Executes following checks:
            1. Argument `exception_classes` must be of type `tuple`, `list` or `set`.
            2. All elements of `exception_classes` must be subclasses of `Exception`.

        Args:
            N/A
        Returns:
            None
        Raises:
            TypeError: Raised if `exception_classes` is not of type `tuple`, `list` or `set`
            TypeError: Raised if any element of `exception_classes` is not subclass of `Exception`.
        """
        if not isinstance(self.exception_classes, (list, tuple, set)):
            raise TypeError(
                "Parameter `exception_classes` must be `list`, `tuple` or `set`."
            )
        for exception_class in self.exception_classes:
            if not issubclass(exception_class, Exception):
                raise TypeError(
                    "Element of `exception_classes` must be a subclass of `Exception`."
                )

    def __call__(self, func):
        """Invoked on decorator instance call.
        Holds logic of the callback process, including invoking callbacks and passed function.

        Functions:
            wrapper(*func_args, **func_kwargs):
                Decorator class wrapper accepting `args` and `kwargs`
                for the decorated function. Contains callback and execution logic.

        Args:
            func (Callable): Decorated function to be executed amongst callbacks.
        Returns:
            None
        Raises:
            N/A
        """

        def wrapper(*func_args, **func_kwargs):
            """Decorator class wrapper accepting `args` and `kwargs` for the decorated function.
            Contains callback and execution logic.

            Process:
                1. Validation of decorator arguments.
                2. Setting up custom tracer.
                3. Executing `on_call` callback (if defined).
                4. Executing decorated function.
                5. On success:
                    6a. Extracting decorated function local variables.
                    7a. Executing `on_success` callback (if defined).
                    8a. Returning decorated function result
                5. On error (catching exception from `exception_classes`):
                    6b. Extracting decorated function local variables.
                    7b. Executing `on_failure` callback (if defined).
                    8b. Returning `default_return` value
                9. Reverting to default tracer.
                10. Re-raising decorated function exception if `on_end` callback is not defined.
                11. Executing `on_end` callback (if defined).

            Args:
                func_args(tuple): Arguments for the decorated function.
                kwargs(dict): Keyword arguments for the decorated function.
            Returns:
                Any: Decorated function result or `default_return` value.
            Raises:
                func_exception: Raised if error occurs during function execution, only if `on_end`
                    handler is not defined.
            """
            self.validate_arguments()
            sys.setprofile(self.tracer)
            func_exception, func_result, func_scope_vars = None, None, []
            try:
                self.run_on_call_func(func_args, func_kwargs)
                func_result = func(*func_args, **func_kwargs)
                func_scope_vars = self.get_func_scope_vars()
                self.run_on_success_func(func_result, func_args, func_kwargs)
                return func_result
            except self.exception_classes as ex:
                func_exception = ex
                func_scope_vars = self.get_func_scope_vars()
                self.run_on_failure_func(func_exception, func_args, func_kwargs)
                return self.default_return
            finally:
                sys.setprofile(None)
                if self.on_end is _default_callback and func_exception:
                    raise func_exception
                result = func_result if not func_exception else self.default_return
                self.run_on_end_func(
                    result, func_exception, func_args, func_kwargs, func_scope_vars
                )

        return wrapper

    def tracer(self, frame, event, _):
        """Represents tracer for storing local variables from last executed function.
        Upon function return, this tracer saves function locals to `local_vars` instance attribute.

        Args:
            frame (Frame): Frame to be traced.
            event (Event): Event for tracing.
        Returns:
            None
        Raises:
            N/A
        """
        if event == "return":
            self.local_vars = frame.f_locals.copy()

    def run_callback_func(self, func, func_kwargs):
        """Executes given callback function with given kwargs.
        If callback function was decorated with a `@backgroung_callback` decorator,
        function is executed on a new thread in the background.

        Args:
            func (Callable): Callback function to be executed.
            func_kwargs (dict): Keyword arguments to be passed to the callback function.
        Returns:
            None
        Raises:
            N/A
        """
        if hasattr(func, "__background_callpyback__"):
            task = threading.Thread(target=func, args=(), kwargs=func_kwargs)
            task.start()
        else:
            func(**func_kwargs)

    def run_on_call_func(self, func_args, func_kwargs):
        """Generates kwargs for given `on_call` callback function and executes
        it with generated kwargs.

        Args:
            func_args (tuple): Arguments for the decorated function.
            func_kwargs (dict): Keyword arguments for the decorated function.
        Returns:
            None
        Raises:
            N/A
        """
        on_call_kwargs = self.get_on_call_kwargs(func_args, func_kwargs)
        self.run_callback_func(self.on_call, on_call_kwargs)

    def run_on_success_func(self, func_result, func_args, func_kwargs):
        """Generates kwargs for given `on_success` callback function and executes
        it with generated kwargs.

        Args:
            func_args (tuple): Arguments for the decorated function.
            func_kwargs (dict): Keyword arguments for the decorated function.
        Returns:
            None
        Raises:
            N/A
        """
        on_success_kwargs = self.get_on_success_kwargs(
            func_result, func_args, func_kwargs
        )
        self.run_callback_func(self.on_success, on_success_kwargs)

    def run_on_failure_func(self, func_exception, func_args, func_kwargs):
        """Generates kwargs for given `on_failure` callback function and executes
        it with generated kwargs.

        Args:
            func_args (tuple): Arguments for the decorated function.
            func_kwargs (dict): Keyword arguments for the decorated function.
        Returns:
            None
        Raises:
            N/A
        """
        on_failure_kwargs = self.get_on_failure_kwargs(
            func_exception, func_args, func_kwargs
        )
        self.run_callback_func(self.on_failure, on_failure_kwargs)

    def run_on_end_func(
        self, func_result, func_exception, func_args, func_kwargs, func_scope_vars
    ):
        """Generates kwargs for given `on_end` callback function and executes
        it with generated kwargs.

        Args:
            func_args (tuple): Arguments for the decorated function.
            func_kwargs (dict): Keyword arguments for the decorated function.
        Returns:
            None
        Raises:
            N/A
        """
        on_end_kwargs = self.get_on_end_kwargs(
            func_result, func_exception, func_args, func_kwargs, func_scope_vars
        )
        self.run_callback_func(self.on_end, on_end_kwargs)

    def get_func_scope_vars(self):
        """Gets requested decorated function's scope variables, specified in `pass_vars` attribute.
        Any missing requested scope variables will be replaced by `<not-found>` string literal.

        Args:
            N/A
        Returns:
            dict: Names and values map of requested decorated function's scope variables.
        Raises:
            N/A
        """
        func_scope_vars = {}
        if not self.pass_vars:
            return []
        for var_name in self.pass_vars:
            func_scope_vars[var_name] = self.local_vars.get(var_name, "<not-found>")
        self.local_vars = {}
        return func_scope_vars

    def get_on_call_kwargs(self, func_args, func_kwargs):
        """Generates kwargs for `on_call` callback function.
        Only kwargs specified in callback signature will be passed to the callback function.
        This is to allow omitting unused parameters in user created callbacks.

        Args:
            func_args (tuple): Decorated function arguments.
            func_kwargs (dict): Decorated function keyword arguments.

        Returns:
            dict: Keyword arguments for `on_call` callback function.
        """
        kwargs = {}
        params = inspect.signature(self.on_call).parameters
        if "func_args" in params:
            kwargs["func_args"] = func_args
        if "func_kwargs" in params:
            kwargs["func_kwargs"] = func_kwargs
        return kwargs

    def get_on_success_kwargs(self, func_result, func_args, func_kwargs):
        """Generates kwargs for `on_success` callback function.
        Only kwargs specified in callback signature will be passed to the callback function.

        Args:
            func_result (Any): Decorated function result (return value).
            func_args (tuple): Decorated function arguments.
            func_kwargs (dict): Decorated function keyword arguments.

        Returns:
            dict: Keyword arguments for `on_success` callback function.
        """
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
        """Generates kwargs for `on_failure` callback function.
        Only kwargs specified in callback signature will be passed to the callback function.

        Args:
            func_exception (Eception): Exception raised during decorated function execution.
            func_args (tuple): Decorated function arguments.
            func_kwargs (dict): Decorated function keyword arguments.

        Returns:
            dict: Keyword arguments for `on_failure` callback function.
        """
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
        """Generates kwargs for `on_end` callback function.
        Only kwargs specified in callback signature will be passed to the callback function.

        Args:
            func_result (Any): Decorated function result (return value).
            func_exception (Eception): Exception raised during decorated function execution.
            func_args (tuple): Decorated function arguments.
            func_kwargs (dict): Decorated function keyword arguments.

        Returns:
            dict: Keyword arguments for `on_end` callback function.
        """
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
