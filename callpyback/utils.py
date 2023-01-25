def _callback(func, on_success, on_fail, on_end, *func_args, **func_kwargs):
    try:
        func_result = func(*func_args, **func_kwargs)
        on_success()
        return func_result
    except Exception as ex:
        on_fail(ex)
    finally:
        on_end()
