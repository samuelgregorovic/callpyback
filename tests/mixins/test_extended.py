import pytest
from unittest.mock import MagicMock

from callpyback.mixins.extended import ExtendedCallBackMixin
from callpyback.utils import _default_callback


class Test___init__:
    """Class containing tests for __init__ method"""

    def test_constructor_defaults(self):
        """Tests that constructor sets default values correctly."""
        # Mocks
        # Calls
        mixin = ExtendedCallBackMixin()
        # Assertions
        assert mixin
        assert isinstance(mixin, ExtendedCallBackMixin)
        assert mixin.default_return is None
        assert mixin.pass_vars is None
        assert mixin.exception_classes == (Exception,)
        assert mixin.local_vars == {}

    def test_constructor_supplied_values(self):
        """Tests that constructor sets supplied values correctly."""
        # Mocks
        default_return = "default_return"
        pass_vars = ["var1", "var2"]
        exception_classes = (KeyError, ValueError)
        # Calls
        mixin = ExtendedCallBackMixin(
            default_return=default_return,
            pass_vars=pass_vars,
            exception_classes=exception_classes,
        )
        # Assertions
        assert mixin
        assert isinstance(mixin, ExtendedCallBackMixin)
        assert mixin.default_return == "default_return"
        assert mixin.pass_vars == ["var1", "var2"]
        assert mixin.exception_classes == (KeyError, ValueError)
        assert mixin.local_vars == {}


def create_mixin_obj(
    default_return=None,
    pass_vars=None,
    exception_classes=(Exception,),
):
    """Construct instance of BaseCallBackMixin object from supplied or default values."""
    instance = ExtendedCallBackMixin(
        default_return=default_return,
        pass_vars=pass_vars,
        exception_classes=exception_classes,
    )
    return instance


class Test_validate_pass_vars:
    """Class containing tests for validate_pass_vars method"""

    def test_correct(self):
        """Tests that no errors are raised when pass_vars are correct."""
        # Mocks
        mixin_obj = create_mixin_obj(pass_vars=("var1", "var2"))
        # Calls
        mixin_obj.validate_pass_vars()
        # Assertions
        assert True

    def test_empty(self):
        """Tests that no errors are raised when pass_vars is empty."""
        # Mocks
        mixin_obj = create_mixin_obj()
        # Calls
        mixin_obj.validate_pass_vars()
        # Assertions
        assert True

    def test_bad_list_type_error(self):
        """Tests that error is raised when `pass_vars` is not a list, tuple or set."""
        # Mocks
        mixin_obj = create_mixin_obj(pass_vars="bad_type")
        # Calls
        # Assertions
        with pytest.raises(
            TypeError, match="Parameter `pass_vars` must be `list`, `tuple` or `set`."
        ):
            mixin_obj.validate_pass_vars()

    def test_bad_variable_type_error(self):
        """Tests that error is raised when one of `pass_vars` elements is not a string."""
        # Mocks
        mixin_obj = create_mixin_obj(pass_vars=("x", 1))
        # Calls
        # Assertions
        with pytest.raises(
            TypeError, match="Variable in `pass_vars` must be of type `str`."
        ):
            mixin_obj.validate_pass_vars()


class Test_validate_exception_classes:
    """Class containing tests for validate_exception_classes method"""

    def test_list_type_error(self):
        """Tests that error is raised when `exception_classes` is not a list, tuple or set."""
        # Mocks
        mixin_obj = create_mixin_obj(exception_classes="not_a_list")
        # Calls
        # Assertions
        with pytest.raises(
            TypeError,
            match="Parameter `exception_classes` must be `list`, `tuple` or `set`.",
        ):
            mixin_obj.validate_exception_classes()

    def test_not_a_class_error(self):
        """Tests that error is raised when one of the `exception_classes` elements
        is not a class."""
        # Mocks
        mixin_obj = create_mixin_obj(exception_classes=("some_string",))
        # Calls
        # Assertions
        with pytest.raises(
            TypeError,
            match="Element of `exception_classes` must be a class.",
        ):
            mixin_obj.validate_exception_classes()

    def test_exception_type_error(self):
        """Tests that error is raised when one of the `exception_classes` elements
        is not a subclass of `Exception`."""

        # Mocks
        class DummyClass:
            pass

        mixin_obj = create_mixin_obj(exception_classes=(DummyClass,))
        # Calls
        # Assertions
        with pytest.raises(
            TypeError,
            match="Element of `exception_classes` must be a subclass of `Exception`.",
        ):
            mixin_obj.validate_exception_classes()


class Test_get_func_scope_vars:
    """Test get_func_scope_vars method"""

    def test_undefined_pass_vars(self):
        """Tests that `get_func_scope_vars` returns empty dict if `pass_vars` are not defined."""
        # Mocks
        mixin_obj = create_mixin_obj()
        # Calls
        func_scope_vars = mixin_obj.get_func_scope_vars()
        # Assertions
        assert func_scope_vars == {}

    def test_defined_pass_vars(self):
        """Tests that `get_func_scope_vars` returns full dict if `pass_vars` are defined
        and found in function scope variables."""
        # Mocks
        mixin_obj = create_mixin_obj(pass_vars=("var1", "var2"))
        mixin_obj.local_vars = {"var1": "value1", "var3": "value3"}
        # Calls
        func_scope_vars = mixin_obj.get_func_scope_vars()
        # Assertions
        assert func_scope_vars == {"var1": "value1", "var2": "<not-found>"}


class Test_set_tracer_profile:
    """Test set_tracer_profile method."""

    def test_default_tracer(self):
        """Tests that setting tracer profile executes successfully."""
        # Mocks
        mixin_obj = create_mixin_obj()
        # Calls
        mixin_obj.set_tracer_profile(None)
        # Assertions
        assert True


class Test_tracer:
    """Test tracer method"""

    def test_return_event(self):
        """Tests that local scope variables are extracted and saved to
        the instance attribute when `return` event is triggered."""
        # Mocks
        mixin_obj = create_mixin_obj()

        class DummyFrame:
            def __init__(self, f_locals):
                self.f_locals = f_locals

        frame = DummyFrame({"x": "y"})
        assert mixin_obj.local_vars == {}
        # Calls
        mixin_obj.tracer(frame, "return", None)
        # Assertions
        assert mixin_obj.local_vars == {"x": "y"}

    def test_other_event(self):
        """Test that other events than `return` are ignored."""
        # Mocks
        mixin_obj = create_mixin_obj()

        class DummyFrame:
            def __init__(self, f_locals):
                self.f_locals = f_locals

        frame = DummyFrame({"x": "y"})
        assert mixin_obj.local_vars == {}
        # Calls
        mixin_obj.tracer(frame, "yield", None)
        # Assertions
        assert mixin_obj.local_vars == {}
