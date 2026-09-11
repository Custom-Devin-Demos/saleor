from collections import defaultdict
from collections.abc import Iterable
from uuid import UUID

from ..graphql.core.dataloaders import DataLoader
from .models import Payment


class PaymentsByOrderIdLoader(DataLoader[UUID, list[Payment]]):
    context_key = "payments_by_order"

    def batch_load(self, keys: Iterable[UUID]) -> list[list[Payment]]:
        payments = (
            Payment.objects.using(self.database_connection_name)
            .filter(order_id__in=keys)
            .order_by("pk")
        )
        payment_map: defaultdict[UUID | None, list[Payment]] = defaultdict(list)
        for payment in payments.iterator(chunk_size=1000):
            payment_map[payment.order_id].append(payment)
        return [payment_map.get(order_id, []) for order_id in keys]
