"""Module containing CallPyBack implementation"""

from callpyback.utils import _default_callback, args_to_kwargs
from callpyback.mixins.base import BaseCallBackMixin
from callpyback.mixins.extended import ExtendedCallBackMixin


class CallPyBack(BaseCallBackMixin, ExtendedCallBackMixin):
    """Class implementing callback decorator.

    Attributes:
        N/A

    Methods:
        validate_arguments():
            Runs validation functions for constructor arguments.
        validate_across_mixins():
            Performs cross-mixin validation, which cannot be tested separately.
        __call__(func):
            Invoked on decorator instance call.
        main(func, *args, **kwargs):
            Contains the actual callback logic.
    """

    def __init__(self, **kwargs):
        """Class constructor. Sets instance variables.

        Args:
            on_call (Callable, optional): Called before function execution.
                Defaults to DEFAULT_ON_CALL_LAMBDA.
            on_success (Callable, optional): Called after successfull run.
                Defaults to DEFAULT_ON_SUCCESS_LAMBDA.
            on_failure (Callable, optional): Called after run with errors.
                Defaults to DEFAULT_ON_FAILURE_LAMBDA.
            on_end (Callable, optional): Called after every execution.
                Defaults to DEFAULT_ON_END_LAMBDA.
            default_return (Any, optional): Result to be returned in
                case of error or no return. Defaults to None.
            pass_vars (list|tuple|set, optional): Variable names to be passed
                to `on_end` callback. Defaults to None.
            exception_classes (list|tuple|set): Exception classes to be caught.
                Defaults to (Exception,).

        Returns:
            CallPyBack: decorator instance
        Raises:
            N/A
        """
        super().__init__(**kwargs)

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
        self.validate_across_mixins()

    def validate_across_mixins(self):
        """Performs cross-mixin validation, which cannot be tested separately.

        Executes following checks:
            1. If `pass_vars` is defined, `on_end` must be defined.

        Args:
            N/A
        Returns:
            None
        Raises:
            RuntimeError: Raised if `pass_vars` is defined but `on_end`
            callback is not.
        """
        if self.pass_vars and self.on_end is _default_callback:
            raise RuntimeError(
                "If `pass_vars` is defined, `on_end` must be defined.",
            )

    def __call__(self, func):
        """Invoked on decorator instance call.
        Holds logic of the callback process, including invoking callbacks
        and passed function.

        Functions:
            wrapper(*func_args, **func_kwargs):
                Decorator class wrapper accepting `args` and `kwargs`
                for the decorated function. Contains callback logic.

        Args:
            func (Callable): Decorated function to be executed.
        Returns:
            None
        Raises:
            N/A
        """

        def _wrapper(*func_args, **func_kwargs):
            """Decorator class wrapper accepting `args` and `kwargs` for the
            decorated function.
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
            10. Re-raising decorated function exception if `on_end` callback
                is not defined.
            11. Executing `on_end` callback (if defined).

        Args:
            func(Callable): Decorated function to be executed.
            func_args(tuple): Arguments for the decorated function.
            func_kwargs(dict): Keyword arguments for the decorated function.
        Returns:
            Any: Decorated function result or `default_return` value.
        Raises:
            func_exception: Raised if error occurs during function execution,
            only if `on_end` handler is not defined.
        """
        self.validate_arguments()
        self.set_tracer_profile(self.tracer)
        all_func_kwargs = args_to_kwargs(func, func_args, func_kwargs)
        func_exception, func_result, func_scope_vars = None, None, []
        try:
            self.run_on_call_func(func, all_func_kwargs)
            func_result = func(**all_func_kwargs)
            func_scope_vars = self.get_func_scope_vars()
            self.run_on_success_func(func, func_result, all_func_kwargs)
            return func_result
        except self.exception_classes as ex:
            func_exception = ex
            func_scope_vars = self.get_func_scope_vars()
            self.run_on_failure_func(func, func_exception, all_func_kwargs)
            return self.default_return
        finally:
            self.set_tracer_profile(None)
            if self.on_end is _default_callback and func_exception:
                raise func_exception
            result = func_result if not func_exception else self.default_return
            self.run_on_end_func(
                func, result, func_exception, all_func_kwargs, func_scope_vars
            )
