from classes import CallPyBack
import time


def background_callpyback(func):
    func.background_callpyback = True

    return func


# sample callback method
@background_callpyback
def on_call(func_args, func_kwargs):
    time.sleep(1)
    print("call finished")


@background_callpyback
def on_success(func_result, func_args, func_kwargs):
    time.sleep(1)
    print("success finished")


@background_callpyback
def on_failure(func_exception, func_args, func_kwargs):
    time.sleep(1)
    print("failure finished")


@background_callpyback
def on_end(func_result, func_exception, func_args, func_kwargs, func_scope_vars):
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
)


class Treatment:
    pass


@custom_callback
def django_save(model):
    print("running function")
    id = 2
    print("function done")
    return id


id = django_save(model=Treatment)
print("after func execution")
