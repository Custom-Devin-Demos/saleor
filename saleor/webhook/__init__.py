from collections.abc import Callable

from ..core.telemetry import saleor_attributes, tracer


def traced_payload_generator[**P, R](func: Callable[P, R]) -> Callable[P, R]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        operation = f"{func.__name__}"
        with tracer.start_as_current_span(operation) as span:
            span.set_attribute(saleor_attributes.COMPONENT, "payloads")
            return func(*args, **kwargs)

    return wrapper
