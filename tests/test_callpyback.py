"""Module containing tests for CallPyBack implementation
"""
import pytest
from unittest.mock import MagicMock, call

from callpyback.callpyback import CallPyBack, background_callpyback, _default_callback


class Test_background_callback:
    """Class containing tests for background_callback function"""

    def test_attribute_set(self):
        """_summary_"""
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
        """_summary_"""
        # Mocks
        args = (1, 2, 3)
        kwargs = {"var1": 1, "var2": 2}
        # Calls
        _default_callback(*args, **kwargs)
        # Assertions
        assert True


class Test___init__:
    """Class containing tests for __init__ method"""

    def test_constructor_defaults(self):
        """_summary_"""
        # Mocks
        # Calls
        decorator = CallPyBack()
        # Assertions
        assert decorator
        assert isinstance(decorator, CallPyBack)
        assert decorator.on_call == _default_callback
        assert decorator.on_success == _default_callback
        assert decorator.on_failure == _default_callback
        assert decorator.on_end == _default_callback
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
        """_summary_"""
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
        """_summary_"""
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


class Test_validate_callbacks:
    """Class containing tests for validate_callbacks method"""

    def test_correct(self):
        """_summary_"""
        # Mocks
        callpyback_obj = create_callpyback_obj()
        # Calls
        callpyback_obj.validate_callbacks()
        # Assertions
        assert True

    def test_not_callable_error(self):
        """_summary_"""
        # Mocks
        callpyback_obj = create_callpyback_obj(
            on_call="not_callable",
        )
        # Calls
        # Assertions
        with pytest.raises(
            TypeError, match="Callback must be a callable not <class 'str'>."
        ):
            callpyback_obj.validate_callbacks()

    def test_coroutine_error(self):
        """_summary_"""
        # Mocks
        async def test_coroutine():
            pass

        callpyback_obj = create_callpyback_obj(
            on_call=test_coroutine,
        )
        # Calls
        # Assertions
        with pytest.raises(
            TypeError, match="Callback `test_coroutine` cannot be a coroutine."
        ):
            callpyback_obj.validate_callbacks()


class Test_validate_pass_vars:
    """Class containing tests for validate_pass_vars method"""

    def test_correct(self):
        """_summary_"""
        # Mocks
        callpyback_obj = create_callpyback_obj(pass_vars=("var1", "var2"))
        # Calls
        callpyback_obj.validate_pass_vars()
        # Assertions
        assert True

    def test_empty(self):
        """_summary_"""
        # Mocks
        callpyback_obj = create_callpyback_obj()
        # Calls
        callpyback_obj.validate_pass_vars()
        # Assertions
        assert True

    def test_on_end_not_specified_error(self):
        """_summary_"""
        # Mocks
        callpyback_obj = create_callpyback_obj(
            on_end=_default_callback, pass_vars=("var1", "var2")
        )
        # Calls
        # Assertions
        with pytest.raises(
            RuntimeError, match="If `pass_vars` is defined, `on_end` must be defined."
        ):
            callpyback_obj.validate_pass_vars()

    def test_bad_list_type_error(self):
        """_summary_"""
        # Mocks
        callpyback_obj = create_callpyback_obj(pass_vars="bad_type")
        # Calls
        # Assertions
        with pytest.raises(
            TypeError, match="Parameter `pass_vars` must be `list`, `tuple` or `set`."
        ):
            callpyback_obj.validate_pass_vars()

    def test_bad_variable_type_error(self):
        """_summary_"""
        # Mocks
        callpyback_obj = create_callpyback_obj(pass_vars=("x", 1))
        # Calls
        # Assertions
        with pytest.raises(
            TypeError, match="Variable in `pass_vars` must be of type `str`."
        ):
            callpyback_obj.validate_pass_vars()


class Test_validate_exception_classes:
    """Class containing tests for validate_exception_classes method"""

    def test_list_type_error(self):
        """_summary_"""
        # Mocks
        callpyback_obj = create_callpyback_obj(exception_classes="not_a_list")
        # Calls
        # Assertions
        with pytest.raises(
            TypeError,
            match="Parameter `exception_classes` must be `list`, `tuple` or `set`.",
        ):
            callpyback_obj.validate_exception_classes()

    def test_not_a_class_error(self):
        """_summary_"""
        # Mocks
        callpyback_obj = create_callpyback_obj(exception_classes=("some_string",))
        # Calls
        # Assertions
        with pytest.raises(
            TypeError,
            match="Element of `exception_classes` must be a class.",
        ):
            callpyback_obj.validate_exception_classes()

    def test_exception_type_error(self):
        """_summary_"""
        # Mocks
        class DummyClass:
            pass

        callpyback_obj = create_callpyback_obj(exception_classes=(DummyClass,))
        # Calls
        # Assertions
        with pytest.raises(
            TypeError,
            match="Element of `exception_classes` must be a subclass of `Exception`.",
        ):
            callpyback_obj.validate_exception_classes()


class Test___call__:
    """Class containing tests for __call__ method"""

    def test_basic(self):
        """_summary_"""
        # Mocks
        callpyback_obj = create_callpyback_obj()
        callpyback_obj.main = MagicMock()
        func = MagicMock()
        args = ()
        kwargs = {}
        # Calls
        result = callpyback_obj.__call__(func, *args, **kwargs)
        # Assertions
        assert result
        assert callable(result)


class Test_main:
    """Class containing tests for main method"""

    def test_success(self):
        """_summary_"""
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
        """_summary_"""
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
        """_summary_"""
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
    """Test set_tracer_profile method"""

    def test_default_tracer(self):
        """_summary_"""
        # Mocks
        callpyback_obj = create_callpyback_obj()
        # Calls
        callpyback_obj.set_tracer_profile(None)
        # Assertions
        assert True


class Test_tracer:
    """Test tracer method"""

    def test_return_event(self):
        """_summary_"""
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
        """_summary_"""
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


class Test_run_callback_func:
    """Test run_callback_func method"""

    def test_blocking_callback(self):
        """_summary_"""
        # Mocks
        callpyback_obj = create_callpyback_obj()
        func = MagicMock()
        func_kwargs = {"var": "value"}
        # Calls
        callpyback_obj.run_callback_func(func, func_kwargs)
        # Assertions
        func.assert_called_once_with(**func_kwargs)

    def test_background_callback(self):
        """_summary_"""
        # Mocks
        callpyback_obj = create_callpyback_obj()
        mock = MagicMock()
        func_kwargs = {"var": "value"}

        @background_callpyback
        def func(*_, **__):
            mock()

        # Calls
        assert hasattr(func, "__background_callpyback__")
        callpyback_obj.run_callback_func(func, func_kwargs)
        # Assertions
        mock.assert_called_once()


class Test_run_on_call_func:
    """Test run_on_call_func method"""

    def test_basic(self):
        """_summary_"""
        # Mocks
        on_call = MagicMock()
        callpyback_obj = create_callpyback_obj(on_call=on_call)
        func_args = (1, 2, 3)
        func_kwargs = {"var": "value"}
        callpyback_obj.get_on_call_kwargs = MagicMock(return_value={"var1": "value1"})
        callpyback_obj.run_callback_func = MagicMock()
        # Calls
        callpyback_obj.run_on_call_func(func_args, func_kwargs)
        # Assertions
        callpyback_obj.get_on_call_kwargs.assert_called_once_with(
            func_args, func_kwargs
        )
        callpyback_obj.run_callback_func.assert_called_once_with(
            on_call, {"var1": "value1"}
        )


class Test_run_on_success_func:
    """Test run_on_success method"""

    def test_basic(self):
        """_summary_"""
        # Mocks
        on_success = MagicMock()
        callpyback_obj = create_callpyback_obj(on_success=on_success)
        func_args = (1, 2, 3)
        func_kwargs = {"var": "value"}
        func_result = -1
        callpyback_obj.get_on_success_kwargs = MagicMock(
            return_value={"var1": "value1"}
        )
        callpyback_obj.run_callback_func = MagicMock()
        # Calls
        callpyback_obj.run_on_success_func(func_result, func_args, func_kwargs)
        # Assertions
        callpyback_obj.get_on_success_kwargs.assert_called_once_with(
            func_result, func_args, func_kwargs
        )
        callpyback_obj.run_callback_func.assert_called_once_with(
            on_success, {"var1": "value1"}
        )


class Test_run_on_failure_func:
    """Test run_on_failure method"""

    def test_basic(self):
        """_summary_"""
        # Mocks
        on_failure = MagicMock()
        callpyback_obj = create_callpyback_obj(on_failure=on_failure)
        func_args = (1, 2, 3)
        func_kwargs = {"var": "value"}
        func_exception = Exception("some error")
        callpyback_obj.get_on_failure_kwargs = MagicMock(
            return_value={"var1": "value1"}
        )
        callpyback_obj.run_callback_func = MagicMock()
        # Calls
        callpyback_obj.run_on_failure_func(func_exception, func_args, func_kwargs)
        # Assertions
        callpyback_obj.get_on_failure_kwargs.assert_called_once_with(
            func_exception, func_args, func_kwargs
        )
        callpyback_obj.run_callback_func.assert_called_once_with(
            on_failure, {"var1": "value1"}
        )


class Test_run_on_end_func:
    """Test run_on_end method"""

    def test_basic(self):
        """_summary_"""
        # Mocks
        on_end = MagicMock()
        callpyback_obj = create_callpyback_obj(on_end=on_end)
        func_args = (1, 2, 3)
        func_kwargs = {"var": "value"}
        func_result = -1
        func_scope_vars = {"var1": "value1"}
        func_exception = Exception("some error")
        callpyback_obj.get_on_end_kwargs = MagicMock(return_value={"var1": "value1"})
        callpyback_obj.run_callback_func = MagicMock()
        # Calls
        callpyback_obj.run_on_end_func(
            func_result, func_exception, func_args, func_kwargs, func_scope_vars
        )
        # Assertions
        callpyback_obj.get_on_end_kwargs.assert_called_once_with(
            func_result, func_exception, func_args, func_kwargs, func_scope_vars
        )
        callpyback_obj.run_callback_func.assert_called_once_with(
            on_end, {"var1": "value1"}
        )


class Test_get_func_scope_vars:
    """Test get_func_scope_vars method"""

    def test_undefined_pass_vars(self):
        """_summary_"""
        # Mocks
        callpyback_obj = create_callpyback_obj()
        # Calls
        func_scope_vars = callpyback_obj.get_func_scope_vars()
        # Assertions
        assert func_scope_vars == []

    def test_defined_pass_vars(self):
        """_summary_"""
        # Mocks
        callpyback_obj = create_callpyback_obj(pass_vars=("var1", "var2"))
        callpyback_obj.local_vars = {"var1": "value1", "var3": "value3"}
        # Calls
        func_scope_vars = callpyback_obj.get_func_scope_vars()
        # Assertions
        assert func_scope_vars == {"var1": "value1", "var2": "<not-found>"}
