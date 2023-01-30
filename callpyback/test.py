from classes import CallPyBack


# sample callback methods
async def on_call(func_args, func_kwargs):
    print("----------------------")
    print(f"status: START")
    print(f"args: {func_args}")
    print(f"kwargs: {func_kwargs}")


async def on_success(func_result, func_args, func_kwargs):
    print("----------------------")
    print(f"status: SUCCESS")
    print(f"result: {func_result}")
    print(f"args: {func_args}")
    print(f"kwargs: {func_kwargs}")


async def on_failure(func_exception, func_args, func_kwargs):
    print("----------------------")
    print(f"status: FAIL")
    print(f"exception: {func_exception}")
    print(f"args: {func_args}")
    print(f"kwargs: {func_kwargs}")


async def on_end(func_result, func_exception, func_args, func_kwargs, func_scope_vars):
    print("----------------------")
    print(f"status: DONE")
    print(f"result: {func_result}")
    print(f"exception: {func_exception}")
    print(f"args: {func_args}")
    print(f"kwargs: {func_kwargs}")
    print(f"func_scope_vars: {func_scope_vars}")


# custom class instance test
print("#######CUSTOM CLASS TEST#######")


custom_callback = CallPyBack(
    on_call=on_call,
    on_success=on_success,
    on_failure=on_failure,
    on_end=on_end,
    default_return=["default", "return", "list", 8],
    pass_vars={"b", "a", "c"},
)


@custom_callback
def test_custom_cls(x, y):
    print("test custom cls")
    a = 666
    b = 777
    raise Exception("exsss")
    c = 890
    # return 0


result = test_custom_cls(5, y=2)

print(f"----------------------")
print(f"Return value: {result}")
