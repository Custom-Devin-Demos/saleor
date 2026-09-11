from collections.abc import Callable

from promise import Promise


def with_promise_context[**P, R](func: Callable[P, R]) -> Callable[P, R]:
    """Execute function within Promise context.

    Allow to use dataloaders inside the function.
    """

    def wrapper(*args, **kwargs):
        def promise_executor(_):
            return func(*args, **kwargs)

        # Create promise chain
        promise = Promise.resolve(None).then(promise_executor)
        return promise.get()

    return wrapper
