from __future__ import annotations

import strawberry_django
from strawberry import auto, relay

from demo.product.types import ProductType
from demo.user.types import UserType

from .models import Cart, CartItem, Order, OrderItem


@strawberry_django.type(Order, name="Order")
class OrderType(relay.Node):
    user: UserType
    total: auto
    items: list[OrderItemType]


@strawberry_django.type(OrderItem, name="OrderItem")
class OrderItemType(relay.Node):
    product: ProductType
    quantity: auto
    price: auto
    total: auto


@strawberry_django.type(Cart, name="Cart")
class CartType(relay.Node):
    user: UserType
    total: auto
    items: list[CartItemType]


@strawberry_django.type(CartItem, name="CartItem")
class CartItemType(relay.Node):
    product: ProductType
    quantity: auto
    price: auto
    total: auto
