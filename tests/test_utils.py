from callpyback.utils import (
    background_callpyback,
    _default_callback,
    args_to_kwargs,
)


class Test_background_callback:
    """Class containing tests for background_callback function"""

    def test_attribute_set(self):
        """Test whether the background_callback attribute is set
        to the function."""

        # Mocks
        @background_callpyback
        def function_x():
            pass

        # Calls
        function_x()
        # Assertions
        assert hasattr(function_x, "__background_callpyback__")
        assert function_x.__background_callpyback__


class Test__default_callback:
    """Class containing tests for __default_callback function"""

    def test_call(self):
        """Test that _default_callback function executes without errors."""
        # Mocks
        # Calls
        _default_callback()
        # Assertions
        assert True


class Test_args_to_kwargs:
    """Class containing tests for args_to_kwargs function"""

    def test_basic(self):
        """Test that args_to_kwargs function returns a combined kwargs."""
        # Mocks
        args = (1, 2, 3)
        kwargs = {"d": "val1", "e": "val2"}

        def func(a, b, c, d, e):
            pass

        # Calls
        result = args_to_kwargs(func, args, kwargs)
        # Assertions
        assert result == {"a": 1, "b": 2, "c": 3, "d": "val1", "e": "val2"}
