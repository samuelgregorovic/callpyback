def callpyback(
    on_success=lambda: None, on_failure=lambda ex: None, on_end=lambda: None
):
    def wrapper(func):
        def inner(*func_args, **func_kwargs):
            try:
                func_exception, func_result = None, None
                func_result = func(*func_args, **func_kwargs)
                on_success(func_result, func_args, func_kwargs)
                return func_result
            except Exception as ex:
                func_exception = ex
                func_result = None
                on_failure(ex, func_args, func_kwargs)
            finally:
                on_end(func_result, func_exception, func_args, func_kwargs)

        return inner

    return wrapper
