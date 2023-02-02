import pytest
from unittest.mock import MagicMock

from callpyback.mixins.base import BaseCallBackMixin
from callpyback.utils import _default_callback, background_callpyback


class Test___init__:
    """Class containing tests for __init__ method"""

    def test_constructor_defaults(self):
        """Tests that constructor sets default values correctly."""
        # Mocks
        # Calls
        mixin = BaseCallBackMixin()
        # Assertions
        assert mixin
        assert isinstance(mixin, BaseCallBackMixin)
        assert mixin.on_call is _default_callback
        assert mixin.on_success is _default_callback
        assert mixin.on_failure is _default_callback
        assert mixin.on_end is _default_callback
        assert mixin.callbacks == (
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
        # Calls
        mixin = BaseCallBackMixin(
            on_call=on_call,
            on_success=on_success,
            on_failure=on_failure,
            on_end=on_end,
        )
        # Assertions
        assert mixin
        assert isinstance(mixin, BaseCallBackMixin)
        assert mixin.on_call == on_call
        assert mixin.on_success == on_success
        assert mixin.on_failure == on_failure
        assert mixin.on_end == on_end
        assert mixin.callbacks == (
            on_call,
            on_success,
            on_failure,
            on_end,
        )
        on_call.assert_not_called()
        on_success.assert_not_called()
        on_failure.assert_not_called()
        on_end.assert_not_called()


def create_mixin_obj(
    on_call=MagicMock(),
    on_success=MagicMock(),
    on_failure=MagicMock(),
    on_end=MagicMock(),
):
    """Construct instance of BaseCallBackMixin object from supplied or default values."""
    instance = BaseCallBackMixin(
        on_call=on_call,
        on_success=on_success,
        on_failure=on_failure,
        on_end=on_end,
    )
    return instance


class Test_validate_callbacks:
    """Class containing tests for validate_callbacks method"""

    def test_correct(self):
        """Tests that no errors are raised when callbacks are correct."""
        # Mocks
        mixin_obj = create_mixin_obj(
            on_call=_default_callback,
            on_success=_default_callback,
            on_failure=_default_callback,
            on_end=_default_callback,
        )
        # Calls
        mixin_obj.validate_callbacks()
        # Assertions
        assert True

    def test_not_callable_error(self):
        """Tests that error is raised when one of the callbacks is not Callable."""
        # Mocks
        mixin_obj = create_mixin_obj(
            on_call="not_callable",
        )
        # Calls
        # Assertions
        with pytest.raises(
            TypeError, match="Callback must be a callable not <class 'str'>."
        ):
            mixin_obj.validate_callbacks()

    def test_coroutine_error(self):
        """Tests that error is raised when one of the callbacks is a coroutine."""

        # Mocks
        async def test_coroutine():
            pass

        mixin_obj = create_mixin_obj(
            on_call=test_coroutine,
        )
        # Calls
        # Assertions
        with pytest.raises(
            TypeError, match="Callback `test_coroutine` cannot be a coroutine."
        ):
            mixin_obj.validate_callbacks()

    def test_bad_parameters(self):
        """Tests that error is raised when one of the callbacks accepts wrong combination
        of parameters."""

        # Mocks
        def on_call(x, y):
            pass

        mixin_obj = create_mixin_obj(
            on_call=on_call,
        )
        expected_error_message = (
            "Signature of callback `on_call` is invalid.\n"
            "Expected: No parameter or combination of: func_kwargs.\n"
            "Found: x,y."
        )
        # Calls
        # Assertions
        with pytest.raises(AssertionError, match=expected_error_message):
            mixin_obj.validate_callbacks()


class Test_run_callback_func:
    """Test run_callback_func method"""

    def test_blocking_callback(self):
        """Tests that blocking callback executes successfully in a blocking way."""
        # Mocks
        mixin_obj = create_mixin_obj()
        func = MagicMock()
        func_kwargs = {"var": "value"}
        # Calls
        mixin_obj.run_callback_func(func, func_kwargs)
        # Assertions
        func.assert_called_once_with(**func_kwargs)

    def test_background_callback(self):
        """Tests that background callback (marked by @background_callpyback decorator)
        executes successfully on a new thread (in a background)."""
        # Mocks
        mixin_obj = create_mixin_obj()
        mock = MagicMock()
        func_kwargs = {"var": "value"}

        @background_callpyback
        def func(*_, **__):
            mock()

        # Calls
        assert hasattr(func, "__background_callpyback__")
        mixin_obj.run_callback_func(func, func_kwargs)
        # Assertions
        mock.assert_called_once()


class Test_run_on_call_func:
    """Test run_on_call_func method"""

    def test_basic(self):
        """Tests that `on_call` callback function gets its kwargs generated and is called."""
        # Mocks
        on_call = MagicMock()
        mixin_obj = create_mixin_obj(on_call=on_call)
        func_kwargs = {"var": "value"}
        mixin_obj.get_callback_kwargs = MagicMock(return_value={"var1": "value1"})
        mixin_obj.run_callback_func = MagicMock()
        # Calls
        mixin_obj.run_on_call_func(func_kwargs)
        # Assertions
        mixin_obj.get_callback_kwargs.assert_called_once_with(
            callback=on_call, func_kwargs=func_kwargs
        )
        mixin_obj.run_callback_func.assert_called_once_with(on_call, {"var1": "value1"})


class Test_run_on_success_func:
    """Test run_on_success method"""

    def test_basic(self):
        """Tests that `on_success` callback function gets its kwargs generated and is called."""
        # Mocks
        on_success = MagicMock()
        mixin_obj = create_mixin_obj(on_success=on_success)
        func_kwargs = {"var": "value"}
        func_result = -1
        mixin_obj.get_callback_kwargs = MagicMock(return_value={"var1": "value1"})
        mixin_obj.run_callback_func = MagicMock()
        # Calls
        mixin_obj.run_on_success_func(func_result, func_kwargs)
        # Assertions
        mixin_obj.get_callback_kwargs.assert_called_once_with(
            callback=on_success, func_result=func_result, func_kwargs=func_kwargs
        )
        mixin_obj.run_callback_func.assert_called_once_with(
            on_success, {"var1": "value1"}
        )


class Test_run_on_failure_func:
    """Test run_on_failure method"""

    def test_basic(self):
        """Tests that `on_failure` callback function gets its kwargs generated and is called."""
        # Mocks
        on_failure = MagicMock()
        mixin_obj = create_mixin_obj(on_failure=on_failure)
        func_kwargs = {"var": "value"}
        func_exception = Exception("some error")
        mixin_obj.get_callback_kwargs = MagicMock(return_value={"var1": "value1"})
        mixin_obj.run_callback_func = MagicMock()
        # Calls
        mixin_obj.run_on_failure_func(func_exception, func_kwargs)
        # Assertions
        mixin_obj.get_callback_kwargs.assert_called_once_with(
            callback=on_failure,
            func_exception=func_exception,
            func_kwargs=func_kwargs,
        )
        mixin_obj.run_callback_func.assert_called_once_with(
            on_failure, {"var1": "value1"}
        )


class Test_run_on_end_func:
    """Test run_on_end method"""

    def test_basic(self):
        """Tests that `on_end` callback function gets its kwargs generated and is called."""
        # Mocks
        on_end = MagicMock()
        mixin_obj = create_mixin_obj(on_end=on_end)
        func_kwargs = {"var": "value"}
        func_result = -1
        func_scope_vars = {"var1": "value1"}
        func_exception = Exception("some error")
        mixin_obj.get_callback_kwargs = MagicMock(return_value={"var1": "value1"})
        mixin_obj.run_callback_func = MagicMock()
        # Calls
        mixin_obj.run_on_end_func(
            func_result, func_exception, func_kwargs, func_scope_vars
        )
        # Assertions
        mixin_obj.get_callback_kwargs.assert_called_once_with(
            callback=on_end,
            func_result=func_result,
            func_exception=func_exception,
            func_kwargs=func_kwargs,
            func_scope_vars=func_scope_vars,
        )
        mixin_obj.run_callback_func.assert_called_once_with(on_end, {"var1": "value1"})


class Test_get_callback_kwargs:
    """Test get_callback_kwargs method"""

    def test_no_kwargs(self):
        """Tests that `get_callback_kwargs` returns empty dict if no parameters are defined
        in the signature of callback function."""

        # Mocks
        def on_success():
            pass

        func_kwargs = {"var1": "key1"}
        func_result = -1
        mixin_obj = create_mixin_obj(on_success=on_success)
        # Calls
        on_call_kwargs = mixin_obj.get_callback_kwargs(
            callback=on_success, func_kwargs=func_kwargs, func_result=func_result
        )
        # Assertions
        assert on_call_kwargs == {}

    def test_all_kwargs(self):
        """Tests that `get_callback_kwargs` returns all parameters that are defined
        in the signature of callback function."""

        # Mocks
        def on_success(func_result, func_kwargs):
            pass

        func_kwargs = {"var1": "key1"}
        func_result = -1
        mixin_obj = create_mixin_obj(on_success=on_success)
        # Calls
        on_call_kwargs = mixin_obj.get_callback_kwargs(
            callback=on_success, func_result=func_result, func_kwargs=func_kwargs
        )
        # Assertions
        assert on_call_kwargs == {
            "func_kwargs": func_kwargs,
            "func_result": func_result,
        }
