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
