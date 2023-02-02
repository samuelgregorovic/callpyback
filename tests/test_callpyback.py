"""Module containing tests for CallPyBack implementation
"""
import pytest
from unittest.mock import MagicMock, call

from callpyback.callpyback import CallPyBack, _default_callback


class Test___init__:
    """Class containing tests for __init__ method"""

    def test_constructor_defaults(self):
        """Tests that constructor sets default values correctly."""
        # Mocks
        # Calls
        decorator = CallPyBack()
        # Assertions
        assert decorator
        assert isinstance(decorator, CallPyBack)
        assert decorator.on_call is _default_callback
        assert decorator.on_success is _default_callback
        assert decorator.on_failure is _default_callback
        assert decorator.on_end is _default_callback
        assert decorator.default_return is None
        assert decorator.pass_vars is None
        assert decorator.exception_classes == (Exception,)
        assert decorator.local_vars == {}
        assert decorator.callbacks == (
            _default_callback,
            _default_callback,
            _default_callback,
            _default_callback,
        )

    def test_constructor_supplied_values(self):
        """Tests that constructor sets supplied values correctly."""
        # Mocks
        on_call = MagicMock()
        on_success = MagicMock()
        on_failure = MagicMock()
        on_end = MagicMock()
        default_return = "default_return"
        pass_vars = ["var1", "var2"]
        exception_classes = (KeyError, ValueError)
        # Calls
        decorator = CallPyBack(
            on_call=on_call,
            on_success=on_success,
            on_failure=on_failure,
            on_end=on_end,
            default_return=default_return,
            pass_vars=pass_vars,
            exception_classes=exception_classes,
        )
        # Assertions
        assert decorator
        assert isinstance(decorator, CallPyBack)
        assert decorator.on_call == on_call
        assert decorator.on_success == on_success
        assert decorator.on_failure == on_failure
        assert decorator.on_end == on_end
        assert decorator.default_return == "default_return"
        assert decorator.pass_vars == ["var1", "var2"]
        assert decorator.exception_classes == (KeyError, ValueError)
        assert decorator.local_vars == {}
        assert decorator.callbacks == (
            on_call,
            on_success,
            on_failure,
            on_end,
        )
        on_call.assert_not_called()
        on_success.assert_not_called()
        on_failure.assert_not_called()
        on_end.assert_not_called()


def create_callpyback_obj(
    on_call=MagicMock(),
    on_success=MagicMock(),
    on_failure=MagicMock(),
    on_end=MagicMock(),
    default_return=None,
    pass_vars=None,
    exception_classes=(Exception,),
):
    """Construct instance of CallPyBack object from supplied or default values."""
    instance = CallPyBack(
        on_call=on_call,
        on_success=on_success,
        on_failure=on_failure,
        on_end=on_end,
        default_return=default_return,
        pass_vars=pass_vars,
        exception_classes=exception_classes,
    )
    return instance


class Test_validate_arguments:
    """Class containing tests for validate_arguments method"""

    def test_basic(self):
        """Tests that validate_arguments method calls validation methods."""
        # Mocks
        callpyback_obj = create_callpyback_obj()
        callpyback_obj.validate_callbacks = MagicMock()
        callpyback_obj.validate_pass_vars = MagicMock()
        callpyback_obj.validate_exception_classes = MagicMock()
        # Calls
        callpyback_obj.validate_arguments()
        # Assertions
        callpyback_obj.validate_callbacks.assert_called_once()
        callpyback_obj.validate_pass_vars.assert_called_once()
        callpyback_obj.validate_exception_classes.assert_called_once()


class Test_validate_across_mixins:
    """Class containing tests for validate_across_mixins method"""

    def test_on_end_not_specified_error(self):
        """Tests that error is raised when `on_end` is not specified,
        while `pass_vars` are specified."""
        # Mocks
        callpyback_obj = create_callpyback_obj(
            on_end=_default_callback, pass_vars=("var1", "var2")
        )
        # Calls
        # Assertions
        with pytest.raises(
            RuntimeError, match="If `pass_vars` is defined, `on_end` must be defined."
        ):
            callpyback_obj.validate_across_mixins()


class Test___call__:
    """Class containing tests for __call__ method"""

    def test_basic(self):
        """Tests that no errors are raised when `__call__` method is called,
        and that `main` method is executed."""
        # Mocks
        callpyback_obj = create_callpyback_obj()
        callpyback_obj.main = MagicMock()
        func = MagicMock()
        args = ()
        kwargs = {}
        # Calls
        result = callpyback_obj.__call__(func, *args, **kwargs)()
        # Assertions
        assert result
        assert callable(result)
        callpyback_obj.main.assert_called_once_with(func, args, kwargs)


class Test_main:
    """Class containing tests for main method"""

    def test_success(self):
        """Tests that `main` method is executed successfully, with correct
        steps without raising any exceptions."""
        # Mocks
        func = MagicMock(return_value="func_return")
        args = (1, 2, 3)
        kwargs = {"var": "value"}
        callpyback_obj = create_callpyback_obj()
        callpyback_obj.tracer = MagicMock()
        callpyback_obj.validate_arguments = MagicMock()
        callpyback_obj.set_tracer_profile = MagicMock()
        callpyback_obj.run_on_call_func = MagicMock()
        callpyback_obj.get_func_scope_vars = MagicMock(return_value=[])
        callpyback_obj.run_on_success_func = MagicMock()
        callpyback_obj.run_on_failure_func = MagicMock()
        callpyback_obj.run_on_end_func = MagicMock()
        # Calls
        result = callpyback_obj.main(func, args, kwargs)
        # Assertions
        assert result == "func_return"
        callpyback_obj.validate_arguments.assert_called_once()
        callpyback_obj.set_tracer_profile.assert_has_calls(
            [call(callpyback_obj.tracer), call(None)]
        )
        callpyback_obj.run_on_call_func.assert_called_with(args, kwargs)
        func.assert_called_once_with(*args, **kwargs)
        callpyback_obj.get_func_scope_vars.assert_called_once()
        callpyback_obj.run_on_success_func.assert_called_once_with(result, args, kwargs)
        callpyback_obj.run_on_failure_func.assert_not_called()
        callpyback_obj.run_on_end_func.assert_called_once_with(
            result, None, args, kwargs, []
        )

    def test_failure_unhandled_ex(self):
        """Tests that `main` method raises an exception when exception is
        raised in decorated function when `on_end` callback is not specified."""
        # Mocks
        func = MagicMock(side_effect=Exception("some error"))
        args = (1, 2, 3)
        kwargs = {"var": "value"}
        callpyback_obj = create_callpyback_obj(on_end=_default_callback)
        callpyback_obj.tracer = MagicMock()
        callpyback_obj.validate_arguments = MagicMock()
        callpyback_obj.set_tracer_profile = MagicMock()
        callpyback_obj.run_on_call_func = MagicMock()
        callpyback_obj.get_func_scope_vars = MagicMock(return_value=[])
        callpyback_obj.run_on_success_func = MagicMock()
        callpyback_obj.run_on_failure_func = MagicMock()
        callpyback_obj.run_on_end_func = MagicMock()
        # Calls
        with pytest.raises(Exception, match="some error"):
            _ = callpyback_obj.main(func, args, kwargs)
        # Assertions
        callpyback_obj.validate_arguments.assert_called_once()
        callpyback_obj.set_tracer_profile.assert_has_calls(
            [call(callpyback_obj.tracer), call(None)]
        )
        callpyback_obj.run_on_call_func.assert_called_with(args, kwargs)
        func.assert_called_once_with(*args, **kwargs)
        callpyback_obj.get_func_scope_vars.assert_called_once()
        callpyback_obj.run_on_success_func.assert_not_called()
        callpyback_obj.run_on_failure_func.assert_called_once()
        callpyback_obj.run_on_end_func.assert_not_called()

    def test_failure_handled_ex(self):
        """Tests that `main` method does not raise an exception when exception is
        raised in decorated function when on_end callback is specified."""
        # Mocks
        func = MagicMock(side_effect=Exception("some error"))
        args = (1, 2, 3)
        kwargs = {"var": "value"}
        callpyback_obj = create_callpyback_obj()
        callpyback_obj.tracer = MagicMock()
        callpyback_obj.validate_arguments = MagicMock()
        callpyback_obj.set_tracer_profile = MagicMock()
        callpyback_obj.run_on_call_func = MagicMock()
        callpyback_obj.get_func_scope_vars = MagicMock(return_value=[])
        callpyback_obj.run_on_success_func = MagicMock()
        callpyback_obj.run_on_failure_func = MagicMock()
        callpyback_obj.run_on_end_func = MagicMock()
        # Calls
        _ = callpyback_obj.main(func, args, kwargs)
        # Assertions
        callpyback_obj.validate_arguments.assert_called_once()
        callpyback_obj.set_tracer_profile.assert_has_calls(
            [call(callpyback_obj.tracer), call(None)]
        )
        callpyback_obj.run_on_call_func.assert_called_with(args, kwargs)
        func.assert_called_once_with(*args, **kwargs)
        callpyback_obj.get_func_scope_vars.assert_called_once()
        callpyback_obj.run_on_success_func.assert_not_called()
        callpyback_obj.run_on_failure_func.assert_called_once()
        callpyback_obj.run_on_end_func.assert_called_once()


class Test_set_tracer_profile:
    """Test set_tracer_profile method."""

    def test_default_tracer(self):
        """Tests that setting tracer profile executes successfully."""
        # Mocks
        callpyback_obj = create_callpyback_obj()
        # Calls
        callpyback_obj.set_tracer_profile(None)
        # Assertions
        assert True


class Test_tracer:
    """Test tracer method"""

    def test_return_event(self):
        """Tests that local scope variables are extracted and saved to
        the instance attribute when `return` event is triggered."""
        # Mocks
        callpyback_obj = create_callpyback_obj()

        class DummyFrame:
            def __init__(self, f_locals):
                self.f_locals = f_locals

        frame = DummyFrame({"x": "y"})
        assert callpyback_obj.local_vars == {}
        # Calls
        callpyback_obj.tracer(frame, "return", None)
        # Assertions
        assert callpyback_obj.local_vars == {"x": "y"}

    def test_other_event(self):
        """Test that other events than `return` are ignored."""
        # Mocks
        callpyback_obj = create_callpyback_obj()

        class DummyFrame:
            def __init__(self, f_locals):
                self.f_locals = f_locals

        frame = DummyFrame({"x": "y"})
        assert callpyback_obj.local_vars == {}
        # Calls
        callpyback_obj.tracer(frame, "yield", None)
        # Assertions
        assert callpyback_obj.local_vars == {}
