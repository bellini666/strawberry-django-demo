from __future__ import annotations

import strawberry
import strawberry_django
from strawberry_django.relay import ListConnectionWithTotalCount

from demo.product.types import ProductType


@strawberry.type
class Query:
    product: ProductType = strawberry_django.node()
    products: list[ProductType] = strawberry_django.field(pagination=True)
    products_conn: ListConnectionWithTotalCount[ProductType] = (
        strawberry_django.connection()
    )


@strawberry.type
class Mutation: ...
