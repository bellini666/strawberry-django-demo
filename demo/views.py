from __future__ import annotations

from strawberry.django.views import AsyncGraphQLView

from .base.dataloaders import DataLoaders
from .base.types import Context, HttpRequest, HttpResponse


class GraphQLView(AsyncGraphQLView):
    async def get_context(self, request: HttpRequest, response: HttpResponse):
        return Context(
            request=request,
            response=response,
            dataloaders=DataLoaders(),
        )
