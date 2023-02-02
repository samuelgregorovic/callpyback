"""Module containing BaseCallBackMixin implementation"""

import inspect
import threading

from callpyback.utils import _default_callback


class BaseCallBackMixin:
    """Class implementing basic callback features.

    Attributes:
        N/A

    Methods:
        validate_callbacks():
            Validates callbacks passed to class constructor.
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
        **kwargs,
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

        Returns:
            BaseCallBackMixin: mixin instance
        Raises:
            N/A
        """
        super().__init__(**kwargs)
        self.on_call = on_call
        self.on_success = on_success
        self.on_failure = on_failure
        self.on_end = on_end
        self.callbacks = (self.on_call, self.on_success, self.on_failure, self.on_end)

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

    def run_on_call_func(self, func_kwargs):
        """Generates kwargs for given `on_call` callback function and executes
        it with generated kwargs.

        Args:
            func_kwargs (dict): Keyword arguments for the decorated function.
        Returns:
            None
        Raises:
            N/A
        """
        on_call_kwargs = self.get_on_call_kwargs(func_kwargs)
        self.run_callback_func(self.on_call, on_call_kwargs)

    def run_on_success_func(self, func_result, func_kwargs):
        """Generates kwargs for given `on_success` callback function and executes
        it with generated kwargs.

        Args:
            func_result (Any): Result of the decorated function.
            func_kwargs (dict): Keyword arguments for the decorated function.
        Returns:
            None
        Raises:
            N/A
        """
        on_success_kwargs = self.get_on_success_kwargs(func_result, func_kwargs)
        self.run_callback_func(self.on_success, on_success_kwargs)

    def run_on_failure_func(self, func_exception, func_kwargs):
        """Generates kwargs for given `on_failure` callback function and executes
        it with generated kwargs.

        Args:
            func_exception (Exception): Exception raised by the decorated function.
            func_kwargs (dict): Keyword arguments for the decorated function.
        Returns:
            None
        Raises:
            N/A
        """
        on_failure_kwargs = self.get_on_failure_kwargs(func_exception, func_kwargs)
        self.run_callback_func(self.on_failure, on_failure_kwargs)

    def run_on_end_func(
        self, func_result, func_exception, func_kwargs, func_scope_vars
    ):
        """Generates kwargs for given `on_end` callback function and executes
        it with generated kwargs.

        Args:
            func_result (Any): Result of the decorated function.
            func_exception (Exception): Exception raised by the decorated function.
            func_kwargs (dict): Keyword arguments for the decorated function.
            func_scope_vars (dict): Scope variables for the decorated function.
        Returns:
            None
        Raises:
            N/A
        """
        on_end_kwargs = self.get_on_end_kwargs(
            func_result, func_exception, func_kwargs, func_scope_vars
        )
        self.run_callback_func(self.on_end, on_end_kwargs)

    def get_on_call_kwargs(self, func_kwargs):
        """Generates kwargs for `on_call` callback function.
        Only kwargs specified in callback signature will be passed to the callback function.
        This is to allow omitting unused parameters in user created callbacks.

        Args:
            func_kwargs (dict): Decorated function keyword arguments.

        Returns:
            dict: Keyword arguments for `on_call` callback function.
        """
        kwargs = {}
        params = inspect.signature(self.on_call).parameters
        if "func_kwargs" in params:
            kwargs["func_kwargs"] = func_kwargs
        return kwargs

    def get_on_success_kwargs(self, func_result, func_kwargs):
        """Generates kwargs for `on_success` callback function.
        Only kwargs specified in callback signature will be passed to the callback function.

        Args:
            func_result (Any): Decorated function result (return value).
            func_kwargs (dict): Decorated function keyword arguments.

        Returns:
            dict: Keyword arguments for `on_success` callback function.
        """
        kwargs = {}
        params = inspect.signature(self.on_success).parameters
        if "func_result" in params:
            kwargs["func_result"] = func_result
        if "func_kwargs" in params:
            kwargs["func_kwargs"] = func_kwargs
        return kwargs

    def get_on_failure_kwargs(self, func_exception, func_kwargs):
        """Generates kwargs for `on_failure` callback function.
        Only kwargs specified in callback signature will be passed to the callback function.

        Args:
            func_exception (Eception): Exception raised during decorated function execution.
            func_kwargs (dict): Decorated function keyword arguments.

        Returns:
            dict: Keyword arguments for `on_failure` callback function.
        """
        kwargs = {}
        params = inspect.signature(self.on_failure).parameters
        if "func_exception" in params:
            kwargs["func_exception"] = func_exception
        if "func_kwargs" in params:
            kwargs["func_kwargs"] = func_kwargs
        return kwargs

    def get_on_end_kwargs(
        self, func_result, func_exception, func_kwargs, func_scope_vars
    ):
        """Generates kwargs for `on_end` callback function.
        Only kwargs specified in callback signature will be passed to the callback function.

        Args:
            func_result (Any): Decorated function result (return value).
            func_exception (Eception): Exception raised during decorated function execution.
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
        if "func_kwargs" in params:
            kwargs["func_kwargs"] = func_kwargs
        if "func_scope_vars" in params:
            kwargs["func_scope_vars"] = func_scope_vars
        return kwargs
