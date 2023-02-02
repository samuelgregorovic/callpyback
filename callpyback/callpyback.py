"""Module containing CallPyBack implementation"""
import sys

from callpyback.utils import _default_callback
from callpyback.mixins.base import BaseCallBackMixin
from callpyback.mixins.extended import ExtendedCallBackMixin


class CallPyBack(BaseCallBackMixin, ExtendedCallBackMixin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
        main(func, *args, **kwargs):
            Contains the actual callback logic.
        set_tracer_profile(tracer):
            Sets custom tracer profile.
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

        def _wrapper(*func_args, **func_kwargs):
            """Decorator class wrapper accepting `args` and `kwargs` for the decorated function.
            Calling main method containing callback logic."""
            return self.main(func, func_args, func_kwargs)

        return _wrapper

    def main(self, func, func_args, func_kwargs):
        """Contains callback and execution logic.

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
            func(Callable): Decorated function to be executed amongst callbacks.
            func_args(tuple): Arguments for the decorated function.
            kwargs(dict): Keyword arguments for the decorated function.
        Returns:
            Any: Decorated function result or `default_return` value.
        Raises:
            func_exception: Raised if error occurs during function execution, only if `on_end`
                handler is not defined.
        """
        self.validate_arguments()
        self.set_tracer_profile(self.tracer)
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
            self.set_tracer_profile(None)
            if self.on_end is _default_callback and func_exception:
                raise func_exception
            result = func_result if not func_exception else self.default_return
            self.run_on_end_func(
                result, func_exception, func_args, func_kwargs, func_scope_vars
            )

    def set_tracer_profile(self, tracer):
        """Sets custom tracer to the sys profile.

        Args:
            tracer (Tracer): Tracer to be set.
        Returns:
            None
        Raises:
            N/A
        """
        sys.setprofile(tracer)

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
