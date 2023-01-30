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
    default_return=-1,
    pass_vars={"id"},
)


@custom_callback
# async def django_save(model):
#     print("test custom cls")
#     id = 2
#     #    raise Exception("exsss")
#     return id


@custom_callback
def django_save(model):
    print("test custom cls")
    id = 2
    #    raise Exception("exsss")
    return id


class Treatment:
    pass


import asyncio

# result = asyncio.run(django_save(model=Treatment()))
result = django_save(model=Treatment())


print(f"----------------------")
print(f"Return value: {result}")
