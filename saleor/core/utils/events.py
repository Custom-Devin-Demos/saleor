from collections.abc import Callable
from typing import Any

from django.db import transaction

from ...webhook.event_types import WebhookEventAsyncType


def get_is_deferred_payload(event_name: str) -> bool:
    """Return True if the event has deferred payload.

    When the event has deferred payload, the payload will be generated in the Celery
    task during webhook delivery. In such case, any additional sync calls needed to
    generated the payload are also run in this task, and we don't need to call them
    manually before.
    """
    return WebhookEventAsyncType.EVENT_MAP.get(event_name, {}).get(
        "is_deferred_payload", False
    )


# Any: event callables are heterogeneous plugin-manager methods with arbitrary args.
def call_event(
    func_obj: Callable[..., Any], *func_args: Any, **func_kwargs: Any
) -> None:
    """Call webhook event with given args.

    Ensures that in atomic transaction event is called on_commit.
    """
    connection = transaction.get_connection()
    if connection.in_atomic_block:
        transaction.on_commit(lambda: func_obj(*func_args, **func_kwargs))
    else:
        func_obj(*func_args, **func_kwargs)
