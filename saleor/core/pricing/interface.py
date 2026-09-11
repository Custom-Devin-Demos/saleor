from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Generic, Optional, TypeVar, Union

from ...discount import DiscountType

if TYPE_CHECKING:
    from prices import Money

    from ...channel.models import Channel
    from ...checkout.models import CheckoutLine
    from ...discount.models import CheckoutLineDiscount, OrderLineDiscount, Voucher
    from ...order.models import OrderLine
    from ...product.models import (
        Collection,
        Product,
        ProductType,
        ProductVariant,
    )

DiscountT = TypeVar("DiscountT", "OrderLineDiscount", "CheckoutLineDiscount")


@dataclass
class LineInfo(Generic[DiscountT]):
    line: Union["OrderLine", "CheckoutLine"]
    variant: Optional["ProductVariant"]
    product: Optional["Product"]
    product_type: Optional["ProductType"]
    collections: list["Collection"] = field(repr=False)
    channel: "Channel" = field(repr=False)
    discounts: Iterable[DiscountT]
    voucher: Optional["Voucher"]
    voucher_code: str | None

    @property
    def variant_discounted_price(self) -> "Money":
        raise NotImplementedError

    def get_promotion_discounts(self) -> list[DiscountT]:
        return [
            discount
            for discount in self.discounts
            if discount.type in [DiscountType.PROMOTION, DiscountType.ORDER_PROMOTION]
        ]

    def get_catalogue_discounts(self) -> list[DiscountT]:
        return [
            discount
            for discount in self.discounts
            if discount.type == DiscountType.PROMOTION
        ]

    def get_voucher_discounts(
        self,
    ):
        return [
            discount
            for discount in self.discounts
            if discount.type == DiscountType.VOUCHER
        ]
