import time

from callpyback.callpyback import CallPyBack
from callpyback.utils import background_callpyback


# sample callback method
# @background_callpyback
def on_call(func_kwargs):
    time.sleep(1)
    # raise KeyError("s")
    print(func_kwargs)
    print("call finished")


@background_callpyback
def on_success(func_kwargs):
    time.sleep(1)
    print("success finished")


@background_callpyback
def on_failure(func_exception, func_kwargs):
    time.sleep(1)
    print("failure finished")


@background_callpyback
def on_end(func_result, func_exception, func_kwargs, func_scope_vars):
    print(func_scope_vars)
    time.sleep(1)
    print("end finished")


# custom class instance test
print("#######CUSTOM CLASS TEST#######")


custom_callback = CallPyBack(
    on_call=on_call,
    on_success=on_success,
    on_failure=on_failure,
    on_end=on_end,
    default_return=-1,
    pass_vars={"id"},
    exception_classes=(KeyError,),
)


class Treatment:
    pass


@custom_callback
def django_save(x, model):
    print("running function")
    id = 2
    # raise KeyError("x")
    print("function done")
    return id


id = django_save(1, model=Treatment)


print(f"after func execution {id}")
