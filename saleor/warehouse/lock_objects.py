from .models import Allocation, AllocationQueryset, Stock, StockQuerySet


def stock_select_for_update_for_existing_qs(qs: StockQuerySet) -> StockQuerySet:
    return qs.order_by("pk").select_for_update(of=(["self"]))


def stock_qs_select_for_update() -> StockQuerySet:
    return stock_select_for_update_for_existing_qs(Stock.objects.all())


def allocation_with_stock_qs_select_for_update() -> AllocationQueryset:
    return (
        Allocation.objects.select_related("stock")
        .select_for_update(
            of=(
                "self",
                "stock",
            )
        )
        .order_by("stock__pk")
    )
