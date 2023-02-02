"""Utility functions"""
import inspect


def background_callpyback(func):
    """Decorator to mark a callback function as a background task.
    Marking is done by assigning an attribute `background_callpyback` to the decorated function.
    This will cause the callback to be executed in a separate thread without blocking.

    Args:
        func (Callable): Decorated function to be marked as a background task.

    Returns:
        Callable: Decorated function marked as a background task.
    Raises:
        N/A
    """
    func.__background_callpyback__ = True
    return func


def _default_callback(*_, **__):
    """Default callback function to be used when callback function is not provided."""


def args_to_kwargs(func, func_args, func_kwargs):
    """Transforms `args` and `kwargs` to `all_func_kwargs`.

    Args:
        func(Callable): Decorated function to be executed amongst callbacks.
        func_args(tuple): Arguments for the decorated function.
        func_kwargs(dict): Keyword arguments for the decorated function.
    Returns:
        dict: args and kwargs combined into kwargs for decorated function.
    Raises:
        N/A
    """
    all_kwargs = {}
    func_parameters = inspect.signature(func).parameters
    for param, arg in zip(func_parameters.keys(), func_args):
        all_kwargs[param] = arg
    for kwarg_name, kwarg_value in func_kwargs.items():
        all_kwargs[kwarg_name] = kwarg_value
    return all_kwargs
