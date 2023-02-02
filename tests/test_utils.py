from callpyback.utils import background_callpyback, _default_callback


class Test_background_callback:
    """Class containing tests for background_callback function"""

    def test_attribute_set(self):
        """Test whether the background_callback attribute is set to the function."""

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
        args = (1, 2, 3)
        kwargs = {"var1": 1, "var2": 2}
        # Calls
        _default_callback(*args, **kwargs)
        # Assertions
        assert True
