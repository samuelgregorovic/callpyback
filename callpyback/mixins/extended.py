import inspect

from callpyback.utils import _default_callback


class ExtendedCallBackMixin:
    def __init__(
        self,
        default_return=None,
        pass_vars=None,
        exception_classes=(Exception,),
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.default_return = default_return
        self.pass_vars = pass_vars
        self.exception_classes = exception_classes
        self.local_vars = {}

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
