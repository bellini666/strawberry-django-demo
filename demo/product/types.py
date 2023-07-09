from __future__ import annotations

import strawberry_django
from strawberry import UNSET, auto, relay

from .models import Brand, Product, ProductImage


@strawberry_django.filter(Product, lookups=True)
class BrandFilter:
    name: auto


@strawberry_django.type(
    Brand,
    name="Brand",
    filters=BrandFilter,
)
class BrandType(relay.Node):
    name: auto


@strawberry_django.filter(Product, lookups=True)
class ProductFilter:
    name: auto
    kind: auto
    brand: BrandFilter | None = UNSET


@strawberry_django.order(Product)
class ProductOrdering:
    name: auto
    kind: auto


@strawberry_django.type(
    Product,
    name="Product",
    filters=ProductFilter,
    order=ProductOrdering,
)
class ProductType(relay.Node):
    name: auto
    brand: BrandType | None
    kind: auto
    description: auto
    price: auto
    images: list[ProductImageType]


@strawberry_django.type(ProductImage, name="ProductImage")
class ProductImageType(relay.Node):
    @strawberry_django.field(only=["image"])
    def image(self, root: ProductImage) -> str | None:
        return root.image.url if root.image else None
