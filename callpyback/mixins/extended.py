"""Module containing BaseCallBackMixin implementation"""
import sys
import inspect


class ExtendedCallBackMixin:
    """Class implementing callback decorator.

    Attributes:
        N/A

    Methods:
        validate_pass_vars():
            Validates `pass_vars` constructor argument.
        validate_exception_classes():
            Validates `exception_classes` constructor argument.
        get_func_scope_vars():
            Gets requested decorated function's scope variables, specified in `pass_vars` attribute.
    """

    def __init__(
        self,
        default_return=None,
        pass_vars=None,
        exception_classes=(Exception,),
        **kwargs,
    ):
        """Class constructor. Sets instance variables.

        Args:
            default_return (Any, optional): Result to be returned in case of error or no return.
                Defaults to None.
            pass_vars (list|tuple|set, optional): Variable names to be passed to `on_end` callback.
                Defaults to None.
            exception_classes (list|tuple|set): Exception classes to be caught.
                Defaults to (Exception,).

        Returns:
            ExtendedCallBackMixin: mixin instance
        Raises:
            N/A
        """
        super().__init__(**kwargs)
        self.default_return = default_return
        self.pass_vars = pass_vars
        self.exception_classes = exception_classes
        self.local_vars = {}

    def validate_pass_vars(self):
        """Validates `pass_vars` constructor argument.

        Executes following checks:
            1. Parameter `pass_vars` must be `list`, `tuple` or `set`.
            2. Variable in `pass_vars` must be of type `str`.

        Args:
            N/A
        Returns:
            None
        Raises:
            TypeError: Raised if `pass_vars` is not of type `list`, `tuple` or `set`.
            TypeError: Raised if one of variables in `pass_vars` is not of type `str`.
        """
        if not self.pass_vars:
            return
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
            if not inspect.isclass(exception_class):
                raise TypeError("Element of `exception_classes` must be a class.")
            if not issubclass(exception_class, Exception):
                raise TypeError(
                    "Element of `exception_classes` must be a subclass of `Exception`."
                )

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
            return {}
        for var_name in self.pass_vars:
            func_scope_vars[var_name] = self.local_vars.get(var_name, "<not-found>")
        self.local_vars = {}
        return func_scope_vars

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
