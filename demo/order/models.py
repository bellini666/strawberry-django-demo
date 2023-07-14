from __future__ import annotations

import decimal
from typing import TYPE_CHECKING

import strawberry
from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from django_choices_field.fields import TextChoicesField
from strawberry_django.descriptors import model_property

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager

    from demo.product.models import Product  # noqa: F401
    from demo.user.models import User


class Order(models.Model):
    """Order model."""

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    items: RelatedManager[OrderItem]

    user_id: int
    user = models.ForeignKey["User"](
        "user.User",
        verbose_name=_("Customer"),
        on_delete=models.RESTRICT,
        related_name="+",
        db_index=True,
    )
    cart_id: int
    cart = models.OneToOneField["Cart"](
        "Cart",
        verbose_name=_("Cart"),
        on_delete=models.RESTRICT,
        related_name="+",
        db_index=True,
    )

    @model_property(prefetch_related="items")
    def total(self) -> decimal.Decimal:
        return decimal.Decimal(sum(item.total for item in self.items.all()))


class OrderItem(models.Model):
    """Order item model."""

    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Items")
        unique_together = [
            ("order", "product"),
        ]

    order_id: int
    order = models.ForeignKey(
        Order,
        verbose_name=_("Order"),
        on_delete=models.CASCADE,
        related_name="items",
        db_index=True,
    )
    product_id: int
    product = models.ForeignKey["Product"](
        "product.Product",
        verbose_name=_("Product"),
        on_delete=models.RESTRICT,
        related_name="+",
        db_index=True,
    )
    quantity = models.PositiveIntegerField(
        verbose_name=_("Quantity"),
        default=1,
        blank=True,
        validators=[MinValueValidator(1)],
    )
    price = models.DecimalField(
        verbose_name=_("Price"),
        max_digits=24,
        decimal_places=2,
    )

    @model_property(only=["quantity", "price"])
    def total(self) -> decimal.Decimal:
        return self.quantity * self.price


class Cart(models.Model):
    """Cart model."""

    class Meta:
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")

    @strawberry.enum(name="CartStatus")
    class Status(models.TextChoices):
        PENDING = "pending", _("Pending")
        FINISHED = "finished", _("Finished")

    items: RelatedManager[CartItem]

    status = TextChoicesField(
        verbose_name=_("Category"),
        choices_enum=Status,
        default=Status.PENDING,
    )

    @model_property(prefetch_related="items")
    def total(self) -> decimal.Decimal:
        return decimal.Decimal(sum(item.total for item in self.items.all()))

    @transaction.atomic
    def checkout(self, user: User):
        order = Order.objects.create(user=user, cart=self)
        for item in self.items.all():
            order.items.create(
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )

        return order


class CartItem(models.Model):
    """Product image model."""

    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Items")
        unique_together = [
            ("cart", "product"),
        ]

    cart_id: int
    cart = models.ForeignKey(
        Cart,
        verbose_name=_("Cart"),
        on_delete=models.CASCADE,
        related_name="items",
        db_index=True,
    )
    product_id: int
    product = models.ForeignKey["Product"](
        "product.Product",
        verbose_name=_("Product"),
        on_delete=models.RESTRICT,
        related_name="+",
        db_index=True,
    )
    quantity = models.PositiveIntegerField(
        verbose_name=_("Quantity"),
        default=1,
        blank=True,
        validators=[MinValueValidator(1)],
    )

    @model_property(only=["product__price"], select_related=["product"])
    def price(self) -> decimal.Decimal:
        return self.product.price

    @model_property(only=["quantity", "product__price"], select_related=["product"])
    def total(self) -> decimal.Decimal:
        return self.quantity * self.price
