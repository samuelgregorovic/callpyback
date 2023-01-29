from classes import CallPyBack


# sample callback methods
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


async def on_end(func_result, func_exception, func_args, func_kwargs):
    print("----------------------")
    print(f"status: DONE")
    print(f"result: {func_result}")
    print(f"exception: {func_exception}")
    print(f"args: {func_args}")
    print(f"kwargs: {func_kwargs}")


# custom class instance test
print("#######CUSTOM CLASS TEST#######")

custom_callback = CallPyBack(
    on_success=on_success, on_failure=on_failure, on_end=on_end, default_return=[]
)


@custom_callback
def test_custom_cls(x, func_result):
    print("test custom cls")
    raise Exception("exsss")
    # return 0


result = test_custom_cls(5, func_result=2)

print(f"----------------------")
print(f"Return value: {result}")
