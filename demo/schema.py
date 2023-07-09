import strawberry
from strawberry.tools import merge_types
from strawberry_django.optimizer import DjangoOptimizerExtension

from demo.order.schema import Mutation as OrderMutation
from demo.order.schema import Query as OrderQuery
from demo.product.schema import Mutation as ProductMutation
from demo.product.schema import Query as ProductQuery
from demo.user.schema import Mutation as UserMutation
from demo.user.schema import Query as UserQuery

Query = merge_types(
    "Query",
    (
        OrderQuery,
        ProductQuery,
        UserQuery,
    ),
)
Mutation = merge_types(
    "Mutation",
    (
        OrderMutation,
        ProductMutation,
        UserMutation,
    ),
)


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[
        DjangoOptimizerExtension,
    ],
)
